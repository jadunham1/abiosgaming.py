import json
from .exceptions import NoMatchupFound

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
    def matchup(self):
        try:
            self._raw_data['matchup']
        except KeyError:
            raise NoMatchupFound

