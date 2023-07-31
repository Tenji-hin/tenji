import urllib.parse


class RequestBase:
    BASE_URL = "https://myfigurecollection.net/"

    def getPath(self):
        raise NotImplementedError()

    def getMethod(self):
        raise NotImplementedError()

    def build_params_url(self, params={}) -> str:
        params = {k: v for k, v in params.items() if v is not None}
        return urllib.parse.urlencode(params)
