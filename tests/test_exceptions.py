import pytest

from tenji.exceptions.parser_exception import ParserException
from tenji.exceptions.request_exception import RequestException
from tenji.request.item.item import ItemRequest


@pytest.fixture
def request_obj():
    return ItemRequest(198579)


class TestParserException:
    def test_message_is_a_string_naming_the_page(self, request_obj):
        exc = ParserException.from_request(request_obj, ValueError("bad tag"))
        assert isinstance(exc.args[0], str)
        assert "https://myfigurecollection.net/item/198579" in str(exc)

    def test_message_includes_the_underlying_error(self, request_obj):
        exc = ParserException.from_request(request_obj, ValueError("bad tag"))
        assert "bad tag" in str(exc)

    def test_raising_from_the_cause_keeps_it_reachable(self, request_obj):
        cause = ValueError("bad tag")
        with pytest.raises(ParserException) as info:
            try:
                raise cause
            except ValueError as e:
                raise ParserException.from_request(request_obj, e) from e

        assert info.value.__cause__ is cause

    def test_is_an_exception(self):
        assert issubclass(ParserException, Exception)


class TestRequestException:
    def test_message_is_a_string_naming_the_request(self, request_obj):
        exc = RequestException.from_request(request_obj, OSError("timed out"))
        assert isinstance(exc.args[0], str)
        assert "https://myfigurecollection.net/item/198579" in str(exc)
        assert "timed out" in str(exc)

    def test_raising_from_the_cause_keeps_it_reachable(self, request_obj):
        cause = OSError("timed out")
        with pytest.raises(RequestException) as info:
            try:
                raise cause
            except OSError as e:
                raise RequestException.from_request(request_obj, e) from e

        assert info.value.__cause__ is cause
