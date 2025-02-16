import requests
import pydantic
import urllib.parse as urlparse

from socket import gethostname
from typing import Union, List
from linkwarden_companion.models import (BaseModel,
                                         ALL_MODELS,
                                         Link,
                                         NewLink)
from linkwarden_companion.config import LINKWARDEN_COMPANION_CONFIG


class Linkwarden:
    """
    Linkwarden API client
    """
    SESSION_NAME = f"linkwarden-companion @ {gethostname()}"

    def __init__(self, host: str, user: str, token: str):
        self.host = host
        self.user = user
        self.access_token = token
        self.api_base = urlparse.urljoin(self.host, 'api/v1/')
        self._token = None
        self.token = token

    def authenticate(self) -> dict:
        response = requests.post(urlparse.urljoin(self.api_base, 'session'),
                                 data={
                                     'username': self.user,
                                     'password': self.access_token,
                                     'session_name': self.SESSION_NAME
                                 })
        breakpoint()
        response.raise_for_status()
        return response.json()

    """
    @property
    def token(self):
        \"""
        Must authenticate with the API first, to obtain JWT
        :return:
        \"""
        if self._token is None:
            self._token = self.authenticate()['token']

        return self._token
    """

    @staticmethod
    def parse_models(data: dict) -> BaseModel:
        """
        Parse JSON data to models, should automatically parse nested models,
        as well as automatically determine the model type
        :param data: JSON data
        :return:
        """
        for model in ALL_MODELS:
            try:
                return model.parse_obj(data)
            except pydantic.ValidationError:
                pass
        raise ValueError("Could not parse data to any model")

    @classmethod
    def get_instance(cls):
        return cls(LINKWARDEN_COMPANION_CONFIG['AUTH']['HOST'],
                   LINKWARDEN_COMPANION_CONFIG['AUTH']['USER'],
                   LINKWARDEN_COMPANION_CONFIG['AUTH']['ACCESS_TOKEN'])

    def get(self, endpoint: str):
        """
        Perform a GET request
        :param endpoint: API endpoint
        :return: JSON response
        """
        response = requests.get(urlparse.urljoin(self.api_base, endpoint),
                                headers={'Authorization': f"Bearer {self.token}"})
        return response.json()['response']

    def post(self, endpoint: str, data: dict):
        """
        Perform a POST request
        :param endpoint: API endpoint
        :param data: JSON data
        :return: JSON response
        """
        response = requests.post(urlparse.urljoin(self.api_base, endpoint),
                                 headers={'Authorization': f"Bearer {self.token}"},
                                 json=data)
        return response.json()

    def delete(self, endpoint: str):
        """
        Perform a DELETE request
        :param endpoint: API endpoint
        :return: JSON response
        """
        response = requests.delete(urlparse.urljoin(self.api_base, endpoint),
                                   headers={'Authorization': f"Bearer {self.token}"})
        return response.json()

    def put(self, endpoint: str, data: dict):
        """
        Perform a PUT request
        :param endpoint: API endpoint
        :param data: JSON data
        :return: JSON response
        """
        response = requests.put(urlparse.urljoin(self.api_base, endpoint),
                                headers={'Authorization': f"Bearer {self.token}"},
                                json=data)
        return response.json()

    def patch(self, endpoint: str, data: dict):
        """
        Perform a PATCH request
        :param endpoint: API endpoint
        :param data: JSON data
        :return: JSON response
        """
        response = requests.patch(urlparse.urljoin(self.api_base, endpoint),
                                  headers={'Authorization': f"Bearer {self.token}"},
                                  json=data)
        return response.json()

    def get_links(self) -> List[Link]:
        """
        Get all links
        :return: JSON response
        """
        raw_links = self.get('links')
        return [Link.parse_obj(link) for link in raw_links]

    def get_link(self, link_id: int) -> Link:
        """
        Get a single link
        :param link_id: ID of link
        :return: JSON response
        """
        raw_link = self.get(f'links/{link_id}')
        return Link.parse_obj(raw_link)

    def create_link(self, link: Union[dict, NewLink]) -> Link:
        """
        Create a NewLink
        :param link: Link model
        :return: JSON response
        """
        raw_link = self.post('links', link.dict() if isinstance(link, NewLink) else link)
        return Link.parse_obj(raw_link)
