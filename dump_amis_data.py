import json
import os

from const import FRONTEND_PATH, PGLD_CONTACT_ADDRESS, PIRATE_CONTRACT_ADDRESS, ITEM_CONTRACT_ADDRESS
from loader import Loader


def format_items(items: [dict]):
    def format_item(item):
        for trait in item['traits']:
            item[trait['metadata']['name']] = trait['value']
        item['tokenId'] = int(item['tokenId'])
        item['numOwners'] = int(item['numOwners'])
        item['currentSupply'] = int(item['currentSupply'])
        if 'image_trait' in item:
            cid = item['image_trait'][7:]
            item['image_trait'] = 'https://dweb.link/ipfs/' + cid
        if 'rarity' in item:
            item['rarity'] = int(item['rarity'])
        del item['traits']
        return item
    return list(map(format_item, items))


def format_loot_tables(loot_tables, items):
    item_map = dict(map(lambda x: (x['tokenId'], x), items))

    def format_loot_set_item(loot_set_item):
        if loot_set_item['lootType'] == 'ERC20' and loot_set_item['tokenContract']['id'] == PGLD_CONTACT_ADDRESS:
            return {
                'lootType': 'ERC20',
                'name': 'PGLD',
                'amount': int(int(loot_set_item['amount']) / 1e18),
            }
        elif loot_set_item['lootType'] == 'ERC721' and loot_set_item['tokenContract']['id'] == PIRATE_CONTRACT_ADDRESS:
            pass  # TODO
        elif loot_set_item['lootType'] == 'ERC1155' and loot_set_item['tokenContract']['id'] == ITEM_CONTRACT_ADDRESS:
            item = item_map[int(loot_set_item['lootId'])]
            return {
                'lootType': 'ERC1155',
                'name': item['name'],
                'image': None if 'image_trait' not in item else item['image_trait'],
                'amount': int(loot_set_item['amount']),
            }
        else:
            raise Exception('Unknown loot: ' + loot_set_item)

    def format_loot_item(loot):
        ret = {
            'id': int(loot['id']),
            'group': [],
        }
        for i, loot_set_items in enumerate(loot['lootSets']):
            ret['group'].append({
                'items': list(map(format_loot_set_item, loot_set_items['loots'])),
                'max_supply': int(loot['maxSupply'][i]),
                'percentage': int(loot['weights'][i]) / 100,
                'mints': int(loot['mints'][i]),
            })
        return ret
    return list(map(format_loot_item, loot_tables))


def dump_quests(quests):
    print(quests)


def write_list_to_json_file(filename: str, data: [dict]):
    fp = open(os.path.join(FRONTEND_PATH, filename), 'w')
    fp.write(json.dumps({
        'status': 0,
        'msg': 'ok',
        'data': {
            'items': data,
            'total': len(data),
        },
    }, ensure_ascii=False, sort_keys=False, separators=(',', ':')))
    fp.close()


def main():
    loader = Loader()
    items = loader.get_game_items()
    items = format_items(items)
    write_list_to_json_file('items.json', items)

    loot_tables = loader.get_loot_tables()
    loot_tables = format_loot_tables(loot_tables, items)
    write_list_to_json_file('loot_tables.json', loot_tables)

    quests = loader.get_quests()
    dump_quests(quests)


if __name__ == '__main__':
    main()
