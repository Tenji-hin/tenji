from tenji.request.request_base import RequestBase


class ParserException(Exception):
    def __init__(self, message):
        super().__init__(message)

    @staticmethod
    def from_request(request: RequestBase, previous: Exception):
        msg = ParserException(f"Failed to parse {request.getPath()}")
        return ParserException(msg).with_traceback(previous.__traceback__)
