from .base_client import BaseAbiosClient



class AbiosClient(BaseAbiosClient):
    """
    Simple client for interacting with the AbiosGaming API
    """
    def get_upcoming_matches(
            self, count=3, addons=[],
            games=[], sort='ASC'):
        """
        Gets upcoming matches from AbiosGaming API
        Upcoming matches are matches which have not started yet, but do have a start date

        :param int count: (optional), number of matches to retrieve Default: 3
        :param list(str) str addons: (optional), addons to information you want for the matches i.e. tournaments, matchups
        :param list(int) int games: (optional), numberical value of games to retrieve
        :param str sort: (optional), the order in which items are sorted (ASC or DESC).  Default ASC
        """
        return self._get_matches({"with[]": addons,
                                  "games[]": games,
                                  "starts_after": "now",
                                  "sort": sort},
                                 count=count)

    def get_current_matches(
            self, count=3, addons=[],
            games=[], sort='ASC'):
        return self._get_matches({"with[]": addons,
                                  "games[]": games,
                                  "starts_before": "now",
                                  "ends_after": "now",
                                  "sort": sort},
                                 count=count)

    def get_games(self, order="id", sort="ASC"):
        return self._get_games({"order": order, "sort": sort})

    def get_tournaments(self):
        return self._get_tournaments({})

    def get_competitors(self):
        return self._get_competitors({})
