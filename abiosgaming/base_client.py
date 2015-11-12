import json
import logging
import os.path
import requests
from requests.exceptions import HTTPError, ConnectionError
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError

DEFAULT_ENDPOINT = 'https://api.abiosgaming.com'
DEFAULT_VERSION = 'v1'
logging.basicConfig(level=logging.DEBUG)

class BaseAbiosClient(object):
    def __init__(self, retries=3):
        self._endpoint = DEFAULT_ENDPOINT
        self.session = requests.Session()
        retry = Retry(
            total=retries,
            status_forcelist=[500],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount(self._endpoint, adapter)

    @property
    def _get_access_token(self):
        return "u8vhWfs07Y7PuhdSJAqyPYKbDAHsZdNKW6Df9WYJ";

    def _build_url(self, path):
        return '/'.join([self._endpoint] + path)

    def _call(self, url, response_type='iter', **parameters):
        response_types = ('iter', 'json')
        assert response_type in response_types

        # Get our response using the session
        try:
            response = self.session.get(url,
                                        params=parameters,
                                        verify=True,
                                        stream=True)
        except MaxRetryError as e:
            logging.exception(e)
            raise e

        logging.debug(response)
        logging.debug(response.headers['link'])
        logging.debug(response.links["next"])
        logging.debug(response.links["last"])
        try:
            response.raise_for_status()  # this will raise on 4xx and 5xxs
        except HTTPError as e:
            logging.exception(e)
            raise e

        data = response.json()
        return data

    def _get_matches(self, parameters):
        path = ['v1', 'matches']
        url = self._build_url(path)
        parameters['access_token'] = self._get_access_token
        return self._call(url, **parameters)
