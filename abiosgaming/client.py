from .base_client import BaseAbiosClient
from .match import Match

DEFAULT_NUM_ITEMS = 3

class AbiosClient(BaseAbiosClient):
    """
    Simple client for interacting with the AbiosGaming API
    """
    def get_matches(
            self, count=DEFAULT_NUM_ITEMS, addons=[],
            games=[], competitors=[],
            tournaments=[], substages=[],
            order=None, sort=None, starts_after=None,
            starts_before=None, ends_after=None, ends_before=None):
        return [Match(data) for data in self._get_matches({"with[]": addons,
                                  "games[]": games,
                                  "competitors[]": competitors,
                                  "tournaments[]": tournaments,
                                  "substages[]": substages,
                                  "starts_after": starts_after,
                                  "starts_before": starts_before,
                                  "ends_after": ends_after,
                                  "ends_before": ends_before,
                                  "sort": sort},
                                  count=count)]


    def get_upcoming_matches(
            self, count=DEFAULT_NUM_ITEMS, addons=[],
            games=[], competitors=[],
            tournaments=[], substages=[],
            order='start', sort='ASC'):
        """
        Gets upcoming matches from AbiosGaming API
        Upcoming matches are matches which have not started yet, but do have a start date

        :param int count: (optional), number of matches to retrieve Default: 3
        :param list(str) str addons: (optional), addons to information you want for the matches i.e. tournaments, matchups
        :param list(int) int games: (optional), id of games to retrieve
        :param list(int) int competitors: (optional), id for competitors
        :param list(int) int tournaments: (optional), id for tournament
        :param list(int) int substages: (optional), id of substage of a tournament
        :param str order: (optional), the parameter by which you want to order the matches (start or end). Default start.
        :param str sort: (optional), the order in which items are sorted (ASC or DESC).  Default ASC
        """
        return self.get_matches(count=count,
                                addons=addons,
                                games=games,
                                competitors=competitors,
                                tournaments=tournaments,
                                substages=substages,
                                order=order,
                                sort=sort,
                                starts_after='now')


    def get_recent_results(
            self, count=DEFAULT_NUM_ITEMS, addons=[],
            games=[], competitors=[],
            tournaments=[], substages=[],
            order='end', sort='DESC'):
        """
        Gets recent results from AbiosGaming API
        Upcoming matches are matches which have not started yet, but do have a start date

        :param int count: (optional), number of matches to retrieve Default: 3
        :param list(str) str addons: (optional), addons to information you want for the matches i.e. tournaments, matchups
        :param list(int) int games: (optional), id of games to retrieve
        :param list(int) int competitors: (optional), id for competitors
        :param list(int) int tournaments: (optional), id for tournament
        :param list(int) int substages: (optional), id of substage of a tournament
        :param str order: (optional), the parameter by which you want to order the matches (start or end). Default end.
        :param str sort: (optional), the order in which items are sorted (ASC or DESC).  Default DESC
        """
        return self.get_matches(count=count,
                                addons=addons,
                                games=games,
                                competitors=competitors,
                                tournaments=tournaments,
                                substages=substages,
                                order=order,
                                sort=sort,
                                ends_before='now')

    def get_current_matches(
            self, count=DEFAULT_NUM_ITEMS, addons=[],
            games=[], competitors=[],
            tournaments=[], substages=[],
            order='start', sort='ASC'):
        """
        Gets current matches from AbiosGaming API
        Current matches are matches that have started, but have no yet ended

        :param int count: (optional), number of matches to retrieve Default: 3
        :param list(str) str addons: (optional), addons to information you want for the matches i.e. tournaments, matchups
        :param list(int) int games: (optional), id of games to retrieve
        :param list(int) int competitors: (optional), id for competitors
        :param list(int) int tournaments: (optional), id for tournament
        :param list(int) int substages: (optional), id of substage of a tournament
        :param str order: (optional), the parameter by which you want to order the matches (start or end). Default start.
        :param str sort: (optional), the order in which items are sorted (ASC or DESC).  Default ASC
        """
        return self._get_matches({"with[]": addons,
                                  "games[]": games,
                                  "starts_before": "now",
                                  "ends_after": "now",
                                  "sort": sort},
                                 count=count)

    def get_games(self, order="id", sort="ASC", q=None):
        return self._get_games({"order": order, "sort": sort, 'q': q})

    def get_tournaments(self):
        return self._get_tournaments({})

    def get_competitors(
            self, count=DEFAULT_NUM_ITEMS, q=None,
            games=[], addons=[], tournaments=[],  sort='ASC'):
        """
        Gets competitors from the AbiosGaming API
        A competitor is essentially a team.
        If a team has multiple games i.e. Team Liquid is in multiple games each game will have a different competitor

        :param int count: (optional), number of matches to retrieve Default: 3
        :param list(str) str addons: (optional), addons to information you want for the matches i.e. tournaments, matchups
        :param list(int) int games: (optional), id of games to retrieve
        :param list(int) int tournaments: (optional), id for tournament
        :param str sort: (optional), the order in which items are sorted (ASC or DESC).  Default ASC
        """
        return self._get_competitors({"q": q,
                                      "with[]": addons,
                                      "games[]": games,
                                      "tournaments[]": tournaments,
                                      "sort": sort},
                                     count=count)
