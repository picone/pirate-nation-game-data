import csv
import json
import os

from const import FRONTEND_PATH
from loader import Loader


def dump_items(items):
    fp = open(os.path.join(FRONTEND_PATH, 'items.json'), 'w')
    for i, item in enumerate(items):
        for trait in item['traits']:
            items[i][trait['metadata']['name']] = trait['value']
        items[i]['tokenId'] = int(item['tokenId'])
        items[i]['numOwners'] = int(item['numOwners'])
        items[i]['currentSupply'] = int(item['currentSupply'])
        if 'image_trait' in items[i]:
            cid = items[i]['image_trait'][7:]
            items[i]['image_trait'] = 'https://dweb.link/ipfs/' + cid
        if 'rarity' in items[i]:
            items[i]['rarity'] = int(items[i]['rarity'])
    fp.write(json.dumps({
        'status': 0,
        'msg': 'ok',
        'data': {
            'rows': items,
            'total': len(items),
        },
    }))
    fp.close()


def main():
    loader = Loader()
    items = loader.get_game_items()
    dump_items(items)


if __name__ == '__main__':
    main()
