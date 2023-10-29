import os

GRAPHQL_ENDPOINT = "https://subgraph.satsuma-prod.com/208eb2825ebd/proofofplay/pn-nova/api"

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
GRAPHQL_FILES_PATH = os.path.join(BASE_PATH, 'graphql')
ASSETS_PATH = os.path.join(BASE_PATH, 'assets')
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')
FRONTEND_PATH = os.path.join(BASE_PATH, 'frontend')

PIRATE_CONTRACT_ADDRESS = '0x5b0661b61b0e947e7e49ce7a67abaf8eaafcdc1a'
PGLD_CONTACT_ADDRESS = '0x44bee3b3bb39b22313addc5a574fd13619f267df'
ITEM_CONTRACT_ADDRESS = '0x3b4cdb27641bc76214a0cb6cae3560a468d9ad4a'
