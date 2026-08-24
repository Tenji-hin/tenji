from tenji.request.request_base import RequestBase


class ParserException(Exception):
    @staticmethod
    def from_request(request: RequestBase, previous: Exception) -> "ParserException":
        """Builds an exception describing which page failed to parse.

        Raise it with `from previous` so the underlying error stays reachable
        as __cause__.
        """
        return ParserException(f"Failed to parse {request.get_path()}: {previous}")
