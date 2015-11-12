#!/usr/bin/python2.7

from base_client import BaseAbiosClient

class AbiosClient(BaseAbiosClient):
    def get_upcoming_matches(self,
                             addons=[],
                             games=[],
                             sort='ASC'
                            ):
        return self._get_matches({"with[]": addons, "games[]": games, "starts_after": "now", "sort": sort})

if __name__ == "__main__":
    abios = AbiosClient()
    matches = abios.get_upcoming_matches(addons=['tournament', 'matchups'], games='5')
    print matches[0]

