import logging
import requests
from requests.exceptions import HTTPError, RetryError
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .exceptions import PaginationNotFound
from .utils import named_tuple

DEFAULT_ENDPOINT = 'https://api.abiosgaming.com'
DEFAULT_VERSION = 'v1'


class BaseAbiosClient(object):
    def __init__(self, retries=3):
        self._endpoint = DEFAULT_ENDPOINT
        self.session = requests.Session()
        retry = Retry(
            total=retries,
            status_forcelist=[500],
            method_whitelist= frozenset(['POST', 'GET', 'PUT']),
            backoff_factor=1
        )
        logging.debug("retryable {}".format(retry.is_forced_retry('post', 500)))
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount(self._endpoint, adapter)
        self._access_token = None

    @property
    def access_token(self):
        if not self._access_token:
            logging.debug("Refreshing access token")
            self._access_token = self.refresh_access_token()

        return self._access_token

    @property
    def next_page(self):
        try:
            return self._next_page
        except AttributeError:
            pass

    @next_page.setter
    def next_page(self, value):
        logging.debug("Setting value of next_page to {}".format(value))
        self._next_page = value

    @next_page.deleter
    def next_page(self):
        try:
            del self._next_page
        except AttributeError:
            pass

    def refresh_access_token(self):
        path = ['v1', 'oauth', 'access_token']
        url = self._build_url(path)
        data = self._get_auth_parameters()
        response = self._post(url, data)
        logging.info(response)
        return response['access_token']

    def _get_auth_parameters(self):
        client_id, secret = self.get_credential_set()
        post_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': secret,
        }
        return post_data

    def get_credential_set(self):
        client_id = 'vhVlOflCSOLjMyzAd5eGM7PScyfvIM6TptTCC7Y0'
        client_secret = 'IROG0RVhB2mkIwdvoCjHJ8IOks9lDKbFXB6IeDe0'
        return (client_id, client_secret)

    def _build_url(self, path):
        return '/'.join([self._endpoint] + path)

    def _post(self, url, data):
        try:
            response = self.session.post(url,
                                         data=data,
                                         verify=True)
        except RetryError as e:
            logging.exception(e)
            raise e

        try:
            response.raise_for_status()
        except HTTPError as e:
            logging.exception(e)
            raise e
        return response.json()

    def _call(self, url, **parameters):
        del self.next_page

        # add our access token to the parameters
        parameters['access_token'] = self.access_token
        # Get our response using the session
        try:
            response = self.session.get(url,
                                        params=parameters,
                                        verify=True)
        except RetryError as e:
            logging.exception(e)
            raise e

        if(response.links["next"]["url"]):
            logging.debug("adding next_page: {}".format(response.links["next"]))
            self.next_page = response.links["next"]["url"]

        logging.debug(response.links["next"]["url"])
        try:
            response.raise_for_status()  # this will raise on 4xx and 5xxs
        except HTTPError as e:
            logging.exception(e)
            raise e

        return [named_tuple(item) for item in response.json()]

    def _get_next_page(self):
        if(self.next_page):
            logging.debug("Calling the next URL: {}".format(self.next_page))
            return self._call(self.next_page)
        raise PaginationNotFound

    def _paginated_call(self, url, item_count=3, **parameters):
        self.pagination_max_items = False
        self.pagination_remainder = []
        logging.debug("I'm looking for {} items".format(item_count))
        data = self._call(url, **parameters)
        assert isinstance(data, list)
        logging.debug(len(data))
        while(len(data) < item_count):
            logging.debug("Calling next page")
            try:
                data.extend(self._get_next_page())
            except PaginationNotFound:
                self.pagination_max_items = True
                break
            logging.debug("Data size is now {}".format(len(data)))
        self.pagination_remainder = data[item_count:]
        return [named_tuple(item) for item in data[:item_count]]

    def _get_matches(self, parameters, count=3):
        path = ['v1', 'matches']
        url = self._build_url(path)
        return self._paginated_call(url, item_count=count, **parameters)

    def _get_tournaments(self, parameters, count=3):
        path = ['v1', 'tournaments']
        url = self._build_url(path)
        return self._paginated_call(url, item_count=count, **parameters)

    def _get_competitors(self, parameters, count=3):
        path = ['v1', 'competitors']
        url = self._build_url(path)
        return self._paginated_call(url, item_count=count, **parameters)

    def _get_games(self, parameters):
        path = ['v1', 'games']
        url = self._build_url(path)
        return self._call(url, **parameters)
