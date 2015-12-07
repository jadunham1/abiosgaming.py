import logging
import requests
from requests.exceptions import HTTPError, RetryError
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from .exceptions import PaginationNotFound
from .utils import named_tuple

DEFAULT_ENDPOINT = 'https://api.abiosgaming.com'

log = logging.getLogger(__name__)

class BaseAbiosClient(object):
    def __init__(self, retries=3, client_id=None, secret=None, access_token=None, endpoint=DEFAULT_ENDPOINT):
        self._endpoint = endpoint
        self.session = requests.Session()
        retry = Retry(
            total=retries,
            status_forcelist=[500, 401],
            method_whitelist= frozenset(['POST', 'GET', 'PUT']),
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount(self._endpoint, adapter)
        self._access_token = access_token
        self._client_id = client_id
        self._secret = secret

    @property
    def access_token(self):
        """
        Property: get the access_token for the request
        If there isn't one cached we should go fetch a new one
        """
        if not self._access_token:
            log.debug("Refreshing access token")
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
        log.debug("Setting value of next_page to {}".format(value))
        self._next_page = value

    @next_page.deleter
    def next_page(self):
        try:
            del self._next_page
        except AttributeError:
            pass

    def refresh_access_token(self):
        """
        Gets a new access token given our credentials
        """
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
        return (self._client_id, self._secret)

    def _build_url(self, path):
        """
        Private function to build a url given a path
        """
        return '/'.join([self._endpoint] + path)

    def _post(self, url, data):
        """
        Private function to do a post request to a URL
        """
        try:
            response = self.session.post(url,
                                         data=data,
                                         verify=True)
        except RetryError as e:
            log.exception(e)
            raise e

        try:
            response.raise_for_status()
        except HTTPError as e:
            log.exception(e)
            raise e
        return response.json()

    def _call(self, url, **parameters):
        """
        Private function to do a GET request on a URL from our session

        This function if called removes the next_page from the cache if there is one
        Then makes the call and adds the new pagination if one is returned by the server
        """
        del self.next_page

        # add our access token to the parameters
        parameters['access_token'] = self.access_token
        # Get our response using the session
        try:
            response = self.session.get(url,
                                        params=parameters,
                                        verify=True)
        except RetryError as e:
            log.exception(e)
            raise e

        try:
            response.raise_for_status()  # this will raise on 4xx and 5xxs
        except HTTPError as e:
            log.exception(e)
            raise e

        if('next' in response.links):
            log.debug("adding next_page: {}".format(response.links["next"]))
            self.next_page = response.links["next"]["url"]

        return response.json()

    def _get_next_page(self):
        if(self.next_page):
            log.debug("Calling the next URL: {}".format(self.next_page))
            return self._call(self.next_page)
        raise PaginationNotFound

    def _paginated_call(self, url, item_count=3, **parameters):
        """
        Private function to call a url and get the number of items requested
        The AbiosGaming API puts next, prev, and last pagination in their headers.

        Here we look for item_count number of entires in the first call
        If we don't it was call the paginated data until we have enough to fulfil our request.
        If we can't find enough items we set pagination_max_items so the client will know we tried
        but ran out of items

        We also set a value called pagination_remainder for the client
        This is the remainder of items left.
        Short example:
            You want 17 items
            You get 15 on first call, 15 more on your second call
            You return the 17 items to the client, but the other 13 entries are cached in the
            pagination_remainder until the next time a paginated call is made
        """
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
        return data[:item_count]

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
