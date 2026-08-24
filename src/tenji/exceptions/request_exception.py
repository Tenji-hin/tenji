from tenji.request.request_base import RequestBase


class RequestException(Exception):
    @staticmethod
    def from_request(request: RequestBase, previous: Exception) -> "RequestException":
        """Builds an exception describing which request failed.

        Raise it with `from previous` so the underlying error stays reachable
        as __cause__.
        """
        return RequestException(
            f"Failed to perform request {request.get_path()}: {previous}"
        )
