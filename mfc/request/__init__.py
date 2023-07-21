class RequestBase:
    BASE_URL = "https://myfigurecollection.net/"

    def getPath(self):
        raise NotImplementedError()
