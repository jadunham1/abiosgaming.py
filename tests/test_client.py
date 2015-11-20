from vcr_unittest import VCRTestCase
from abiosgaming.client import AbiosClient
from urllib3.exceptions import MaxRetryError
from requests.exceptions import HTTPError, RetryError
import logging

try:
    from unittest import mock
except ImportError:
    import mock

logging.basicConfig(level=logging.DEBUG)

class AbiosClientTestCase(VCRTestCase):
    def setUp(self):
        super(AbiosClientTestCase, self).setUp()
        self.client = AbiosClient()

    def test_get_upcoming_matches(self):
        matches = self.client.get_upcoming_matches()
        assert isinstance(matches, list)

    def test_get_current_matches(self):
        matches = self.client.get_current_matches()
        assert isinstance(matches, list)

    def test_get_tournaments(self):
        tournaments = self.client.get_tournaments()
        assert isinstance(tournaments, list)

    def test_get_competitors(self):
        competitors = self.client.get_competitors()
        assert isinstance(competitors, list)

    def test_get_games(self):
        games = self.client.get_games()
        assert isinstance(games, list)

    def test_next_page(self):
        del self.client.next_page
        assert not self.client.next_page
        self.client.next_page = "testing123"
        assert isinstance(self.client.next_page, str)

    def test_large_fetch_matches(self):
        matches = self.client.get_upcoming_matches(count=50)
        assert len(matches) == 50

    def test_400s_from_auth(self):
        self.assertRaises(HTTPError, self.client.refresh_access_token)

    def test_400s_from_games(self):
        self.assertRaises(HTTPError, self.client.get_games)

    def test_500s_from_auth(self):
        self.assertRaises(RetryError, self.client.refresh_access_token)

    def test_500s_from_games(self):
        self.assertRaises(RetryError, self.client.get_games)
