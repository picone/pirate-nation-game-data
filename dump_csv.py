import csv
import os

from const import OUTPUT_PATH
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


def main():
    loader = Loader()
    items = loader.get_game_items()
    dump_items(items)


if __name__ == '__main__':
    main()
