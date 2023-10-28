import csv
import os

from const import OUTPUT_PATH, PIRATE_CONTRACT_ADDRESS, PGLD_CONTACT_ADDRESS, ITEM_CONTRACT_ADDRESS
from loader import Loader


def dump_items(items):
    fields = ['id', 'tokenId', 'contractAddress', 'name', 'numOwners', 'currentSupply']
    trait_name_set = set()
    for item in items:
        for trait in item['traits']:
            trait_name_set.add(trait['metadata']['name'])
    for trait_name in trait_name_set:
        fields.append(trait_name)

    fp = open(os.path.join(OUTPUT_PATH, 'items.csv'), 'w', newline='')
    writer = csv.DictWriter(fp, fields)
    writer.writeheader()
    for item in items:
        write_item = {
            'id': item['id'],
            'tokenId': item['tokenId'],
            'contractAddress': item['contractAddress'],
            'name': item['name'],
            'numOwners': item['numOwners'],
            'currentSupply': item['currentSupply'],
        }
        for trait in item['traits']:
            write_item[trait['metadata']['name']] = trait['value']
        writer.writerow(write_item)
    fp.close()


def group_loot_tables(loot_tables):
    ret = []
    for loot in loot_tables:
        new_loot_item = {
            'id': loot['id'],
            'groups': [],
        }
        for i, item in enumerate(loot['lootSets']):
            new_loot_item['groups'].append({
                'loots': item['loots'],
                'max_supply': int(loot['maxSupply'][i]),
                'weights': int(int(loot['maxSupply'][i]) / 100),
                'mints': int(loot['maxSupply'][i]),
            })
        ret.append(new_loot_item)
    return ret


def dump_loot_tables(loot_tables):
    for loot in loot_tables:
        fields = ['id', 'loots', 'max_supply', 'weights', 'mints']
        fp = open(os.path.join(OUTPUT_PATH, 'loot_tables.csv'), 'w', newline='')
        writer = csv.DictWriter(fp, fields)
        writer.writeheader()
        for group in loot['groups']:
            writer.writerow({
                'id': loot['id'],
                'loots': group['loots'],
                'max_supply': group['max_supply'],
                'weights': group['weights'],
                'mints': group['mints'],
            })
        fp.close()


def dump_quests(quests, quest_assets, items):
    fields = ['id', 'name', 'start_description', 'finish_description', 'successXp', 'cooldownSeconds', 'totalCompleted',
              'min_level', 'PGLD', 'generation']
    max_input_count = 0
    for quest in quests:
        input_count = len(list(filter(lambda x: x['tokenPointer']['tokenType'] == 'ERC1155', quest['inputs'])))
        max_input_count = max(max_input_count, input_count)
    for i in range(1, max_input_count + 1):
        fields.append('input_%d' % i)

    fp = open(os.path.join(OUTPUT_PATH, 'quests.csv'), 'w', newline='')
    writer = csv.DictWriter(fp, fields)
    writer.writeheader()
    for quest in quests:
        quest_id = quest['id']
        if quest_id not in quest_assets:
            # raise Exception(f'Quest {quest_id} not found in quest_assets')
            continue
        input_index = 1
        write_item = {
            'id': quest_id,
            'name': quest_assets[quest_id]['name'],
            'start_description': quest_assets[quest_id]['descriptions']['started'],
            'finish_description': quest_assets[quest_id]['descriptions']['finished'],
            'successXp': quest['successXp'],
            'cooldownSeconds': quest['cooldownSeconds'],
            'totalCompleted': quest['totalCompleted'],
        }
        for inp in quest['inputs']:
            if inp['tokenPointer']['tokenType'] == 'ERC721' and inp['tokenPointer']['tokenContract']['id'] == PIRATE_CONTRACT_ADDRESS:
                if inp['traitChecks'][0]['traitMetadata']['name'] == 'level' and inp['traitChecks'][0]['checkType'] == 'GTE':
                    write_item['min_level'] = inp['traitChecks'][0]['traitValue']
                elif inp['traitChecks'][0]['traitMetadata']['name'] == 'generation' and inp['traitChecks'][0]['checkType'] == 'EQ':
                    write_item['generation'] = inp['traitChecks'][0]['traitValue']
                else:
                    raise Exception(f'Unknown trait check {inp["traitChecks"][0]}')
            elif inp['tokenPointer']['tokenType'] == 'ERC20' and inp['tokenPointer']['tokenContract']['id'] == PGLD_CONTACT_ADDRESS:
                write_item['PGLD'] = int(int(inp['tokenPointer']['amount']) / 1e18)
            elif inp['tokenPointer']['tokenType'] == 'ERC1155' and inp['tokenPointer']['tokenContract']['id'] == ITEM_CONTRACT_ADDRESS:
                token_id = inp['tokenPointer']['tokenId']
                if token_id not in items:
                    raise Exception(f'Item {token_id} not found in items')
                write_item['input_%d' % input_index] = '%s x %s' % (
                    items[token_id]['name'],
                    inp['tokenPointer']['amount'],
                )
                input_index += 1
            else:
                raise Exception(f'Unknown input {inp}')
        writer.writerow(write_item)
    fp.close()


def main():
    loader = Loader()
    items = loader.get_game_items()
    dump_items(items)

    item_assets = loader.get_game_item_assets()
    loot_tables = group_loot_tables(loader.get_loot_tables())
    dump_loot_tables(loot_tables)

    quests = loader.get_quests()
    quest_assets = loader.get_quest_assets()
    dump_quests(quests, quest_assets, item_assets)


if __name__ == '__main__':
    main()
