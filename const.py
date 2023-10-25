import os

GRAPHQL_ENDPOINT = "https://subgraph.satsuma-prod.com/208eb2825ebd/proofofplay/pn-nova/api"
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
GRAPHQL_FILES_PATH = os.path.join(BASE_PATH, 'graphql')
ASSETS_PATH = os.path.join(BASE_PATH, 'assets')
OUTPUT_PATH = os.path.join(BASE_PATH, 'output')
