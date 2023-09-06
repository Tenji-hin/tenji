from tenji.request.request_base import RequestBase


class TenjiRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def from_request(request: RequestBase, previous: Exception):
        msg = TenjiRequestException(f"Failed to perform request {request.getPath()}")
        return TenjiRequestException(msg).with_traceback(previous.__traceback__)
