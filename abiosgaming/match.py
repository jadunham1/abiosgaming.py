import json
from .exceptions import NoMatchupFound
from collections import OrderedDict


class Match:
    """
    A match object for abios gaming
    """
    def __init__(self, raw_data):
        self._raw_data = raw_data

    @property
    def start(self):
        return self._raw_data['start']

    @property
    def end(self):
        return self._raw_data['end']

    @property
    def id(self):
        return self._raw_data['id']

    @property
    def title(self):
        return self._raw_data['title']

    @property
    def bestOf(self):
        return self._raw_data['bestOf']

    @property
    def matchups(self):
        try:
            return self._raw_data['matchups']
        except KeyError:
            raise NoMatchupFound

    def get_competitors_name_list(self):
        return [competitor['name']
         for competitor in matchup['competitors']
         for matchup in self.matchups[0]]

    def get_competitor_list(self):
        return self.matchups[0]['competitors']

    def get_score(self):
        score_map = OrderedDict()
        scores = self._get_raw_score()
        for id, score in scores.items():
            score_map[ self.find_competitor_by_id(id)['name'] ] = score

        return score_map

    def _get_raw_score(self):
        return self.matchups[0]['scores']

    def find_competitor_by_id(self, competitor_id):
        competitor_id = int(competitor_id)
        competitors = self.get_competitor_list()
        for competitor in competitors:
            if competitor['id'] == competitor_id:
                return competitor
        raise "Could not find competitor"




