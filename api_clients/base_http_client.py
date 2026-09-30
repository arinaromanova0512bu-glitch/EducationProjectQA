import requests


class BaseHttpClient:
    def __init__(self):
        self.__url = None

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if not value:
            pass
        else:
            self.__url = value

    def _call_method(self, method: str, endpoint: str, **kwargs):
        request = getattr(requests, method.lower())

        response = request(
            url=f"{self.url}{endpoint}",
            verify=False,
            **kwargs
        )

        return response

    def get(self, endpoint: str, **kwargs):
        return self._call_method("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._call_method("POST", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._call_method("DELETE", endpoint, **kwargs)