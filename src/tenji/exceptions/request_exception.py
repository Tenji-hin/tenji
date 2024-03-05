from tenji.request.request_base import RequestBase


class RequestException(Exception):
    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def from_request(request: RequestBase, previous: Exception):
        msg = RequestException(f"Failed to perform request {request.getPath()}")
        return RequestException(msg).with_traceback(previous.__traceback__)
