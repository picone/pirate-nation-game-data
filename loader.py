import json
import os

import gql
from gql.transport import aiohttp

from const import GRAPHQL_ENDPOINT, ASSETS_PATH, GRAPHQL_FILES_PATH


class Loader:
    def __init__(self):
        transport = aiohttp.AIOHTTPTransport(GRAPHQL_ENDPOINT, timeout=30)
        self.__gql_client = gql.Client(transport=transport, fetch_schema_from_transport=True)

    def get_game_items(self) -> list:
        res = self._gql_request('get_game_items')
        return res['gameItems']

    @staticmethod
    def get_game_item_assets() -> dict:
        with open(os.path.join(ASSETS_PATH, 'game_items.json'), 'r') as fp:
            return json.load(fp)

    def get_quests(self) -> list:
        res = self._gql_request('get_quests')
        return res['quests']

    @staticmethod
    def get_quest_assets() -> dict:
        with open(os.path.join(ASSETS_PATH, 'quests.json'), 'r') as fp:
            return json.load(fp)

    def _gql_request(self, name: str):
        with open(os.path.join(GRAPHQL_FILES_PATH, f'{name}.graphql'), 'r') as fp:
            q = fp.read()
        return self.__gql_client.execute(gql.gql(q))
