#!/usr/bin/python2.7

from base_client import BaseAbiosClient


class AbiosClient(BaseAbiosClient):
    def get_upcoming_matches(
            self, count=3, addons=[],
            games=[], sort='ASC'):
        return self._get_matches({"with[]": addons, "games[]": games, "starts_after": "now", "sort": sort}, count=count)

    def get_current_matches(
            self, count=3, addons=[],
            games=[], sort='ASC'):
        return self._get_matches({"with[]": addons, "games[]": games, "starts_before": "now", "ends_after": "now", "sort": sort}, count=count)

    def get_games(self, order="id", sort="ASC"):
        return self._get_games({"order": order, "sort": sort})

    def get_tournaments(self):
        return self._get_tournaments({})

    def get_competitors(self):
        return self._get_competitors({})
