import datetime
import json

import pytest

from tenji.mfc_response import MFCResponse
from tenji.parser.parser_base import ParserBase


def parser_for(html: str) -> ParserBase:
    return ParserBase(MFCResponse(html))


class TestMFCResponse:
    def test_keeps_the_raw_body(self):
        assert MFCResponse("<p>hi</p>").body == "<p>hi</p>"

    def test_soup_is_parsed_on_demand(self):
        response = MFCResponse("<p>hi</p>")
        assert response._soup is None
        assert response.soup.text == "hi"

    def test_soup_is_only_parsed_once(self):
        response = MFCResponse("<p>hi</p>")
        assert response.soup is response.soup


class TestSoup:
    def test_soup_is_parsed_lazily_from_the_response_body(self):
        parser = parser_for("<div id='x'>hello</div>")
        assert parser.try_get_text("#x") == "hello"

    def test_soup_is_only_built_once(self):
        parser = parser_for("<div id='x'>hello</div>")
        assert parser._soup is parser._soup

    def test_parse_html_overrides_the_response_body(self):
        parser = parser_for("<div id='x'>hello</div>")
        parser.parse_html("<div id='x'>goodbye</div>")
        assert parser.try_get_text("#x") == "goodbye"


class TestTryGetTag:
    def test_returns_the_matching_tag(self):
        parser = parser_for("<div class='a'><span>hi</span></div>")
        assert parser.try_get_tag("span").name == "span"

    def test_returns_none_when_missing(self):
        assert parser_for("<div></div>").try_get_tag("span") is None

    def test_searches_within_the_given_parent(self):
        parser = parser_for("<div class='a'><span>a</span></div><div class='b'><span>b</span></div>")
        parent = parser.try_get_tag("div.b")
        assert parser.try_get_tag("span", parent).text == "b"

    def test_returns_the_parent_when_no_selector_is_given(self):
        parser = parser_for("<div class='a'>text</div>")
        parent = parser.try_get_tag("div.a")
        assert parser.try_get_tag(None, parent) is parent


class TestTryGetText:
    def test_returns_text(self):
        assert parser_for("<p>hello</p>").try_get_text("p") == "hello"

    def test_returns_default_when_missing(self):
        assert parser_for("<p>hello</p>").try_get_text("span") is None
        assert parser_for("<p>hello</p>").try_get_text("span", default_value="x") == "x"


class TestTryGetValue:
    def test_returns_attribute_value(self):
        parser = parser_for("<img src='a.jpg' />")
        assert parser.try_get_value("img", "src") == "a.jpg"

    def test_returns_default_when_attribute_is_missing(self):
        parser = parser_for("<img src='a.jpg' />")
        assert parser.try_get_value("img", "alt") is None
        assert parser.try_get_value("img", "alt", default_value="x") == "x"

    def test_returns_default_when_node_is_missing(self):
        assert parser_for("<div></div>").try_get_value("img", "src", default_value=1) == 1


class TestTryGetList:
    def test_splits_on_commas_and_strips(self):
        parser = parser_for("<p>a, b ,c</p>")
        assert parser.try_get_list("p") == ["a", "b", "c"]

    def test_single_value(self):
        assert parser_for("<p>only</p>").try_get_list("p") == ["only"]

    def test_returns_default_when_missing(self):
        assert parser_for("<p>a</p>").try_get_list("span") is None


class TestTryExtractNumber:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("1234", 1234),
            ("1,234 hits", 1234),
            ("Owned (128)", 128),
            ("Item #198579", 198579),
            ("/item/312044", 312044),
            ("category-21", 21),
        ],
    )
    def test_extracts_the_first_number(self, text, expected):
        assert parser_for("").try_extract_number(text) == expected

    def test_returns_default_when_there_is_no_number(self):
        parser = parser_for("")
        assert parser.try_extract_number("no digits here") is None
        assert parser.try_extract_number("no digits here", default_value=0) == 0


class TestTryGetStyleBackground:
    def test_extracts_the_url(self):
        style = "background-image:url(https://example.com/a.jpg);height:10px"
        assert (
            parser_for("").try_get_style_background(style)
            == "https://example.com/a.jpg"
        )

    def test_returns_none_without_a_url(self):
        assert parser_for("").try_get_style_background("height:10px") is None


class TestTryParseMfcTime:
    def test_parses_the_mfc_format_as_utc(self):
        parsed = parser_for("").try_parse_mfc_time("12/21/2017, 13:01:50")
        assert parsed == datetime.datetime(
            2017, 12, 21, 13, 1, 50, tzinfo=datetime.timezone.utc
        )

    @pytest.mark.parametrize("value", [None, "", "yesterday", "2017-12-21"])
    def test_returns_the_default_for_unparseable_input(self, value):
        sentinel = datetime.datetime(2000, 1, 1)
        assert parser_for("").try_parse_mfc_time(value) is None
        assert parser_for("").try_parse_mfc_time(value, sentinel) is sentinel


class TestGetTrailingNumber:
    @pytest.mark.parametrize(
        "text,expected", [("category-15", 15), ("42", 42), ("a1b2", 2)]
    )
    def test_returns_the_trailing_number(self, text, expected):
        assert parser_for("").get_trailing_number(text) == expected

    def test_returns_none_when_the_text_does_not_end_in_a_number(self):
        assert parser_for("").get_trailing_number("category-15a") is None


class TestGetItemIdFromThumbnail:
    def test_extracts_the_id(self):
        url = "https://static.myfigurecollection.net/upload/items/0/198579-4200e.jpg"
        assert parser_for("").get_item_id_from_thumbnail(url) == 198579

    def test_raises_for_an_unexpected_filename(self):
        with pytest.raises(ValueError):
            parser_for("").get_item_id_from_thumbnail("https://example.com/banner.jpg")


class TestTryGetUrlQueryValue:
    def test_returns_the_query_value(self):
        url = "https://myfigurecollection.net/redirect.php?shop=1&jan=4571245296795"
        assert parser_for("").try_get_url_query_value(url, "jan") == "4571245296795"

    def test_returns_default_for_a_missing_key(self):
        url = "https://myfigurecollection.net/redirect.php?shop=1"
        assert parser_for("").try_get_url_query_value(url, "jan") is None
        assert parser_for("").try_get_url_query_value(url, "jan", "x") == "x"

    def test_returns_default_when_there_is_no_query_string(self):
        assert parser_for("").try_get_url_query_value("/item/1", "jan") is None


class TestGetNextSiblingOf:
    def test_returns_the_next_sibling(self):
        parser = parser_for("<div><span class='t'></span>Prepainted</div>")
        assert parser.get_next_sibling_of("span.t").text == "Prepainted"

    def test_returns_none_when_the_node_is_missing(self):
        assert parser_for("<div></div>").get_next_sibling_of("span.t") is None

    def test_returns_none_when_there_is_no_sibling(self):
        parser = parser_for("<div><span class='t'></span></div>")
        assert parser.get_next_sibling_of("span.t") is None


class TestJson:
    def test_parse_json(self):
        assert parser_for("").parse_json('{"a": 1}') == {"a": 1}

    def test_parse_html_from_json_replaces_the_soup(self):
        parser = parser_for("<p>original</p>")
        parser.parse_html_from_json(
            json.dumps({"htmlValues": {"WINDOW": "<p>from json</p>"}})
        )
        assert parser.try_get_text("p") == "from json"

    def test_parse_html_from_json_returns_none_without_html_values(self):
        parser = parser_for("<p>original</p>")
        assert parser.parse_html_from_json(json.dumps({"htmlValues": None})) is None
        assert parser.try_get_text("p") == "original"


PAGINATION_HTML = """
<div class="results-count">
  <div class="results-count-value">177 results</div>
  <div class="results-count-pages">
    <a class="nav-current" href="?page=2">2</a>
    <a class="nav-next" href="?page=3">next</a>
    <a class="nav-last nav-end" href="?page=5">last</a>
  </div>
</div>
"""


class TestTryParsePagination:
    def test_returns_none_without_pagination_controls(self):
        assert parser_for("<div></div>").try_parse_pagination() is None

    def test_parses_a_multi_page_result_set(self):
        pagination = parser_for(PAGINATION_HTML).try_parse_pagination()
        assert pagination.current_page == 2
        assert pagination.has_next_page is True
        assert pagination.total_pages == 5
        assert pagination.total_items == 177

    def test_last_page_has_no_next_page(self):
        html = PAGINATION_HTML.replace('<a class="nav-next" href="?page=3">next</a>', "")
        pagination = parser_for(html).try_parse_pagination()
        assert pagination.has_next_page is False
        assert pagination.total_pages == 5

    def test_falls_back_to_the_current_page_without_a_last_link(self):
        html = PAGINATION_HTML.replace(
            '<a class="nav-last nav-end" href="?page=5">last</a>', ""
        )
        pagination = parser_for(html).try_parse_pagination()
        assert pagination.current_page == 2
        assert pagination.total_pages == 2

    def test_single_page_result_set(self):
        html = """
        <div class="results-count">
          <div class="results-count-value">2 results</div>
        </div>
        """
        pagination = parser_for(html).try_parse_pagination()
        assert pagination.current_page == 1
        assert pagination.has_next_page is False
        assert pagination.total_pages == 1
        assert pagination.total_items == 2

    def test_scopes_to_the_given_parent(self):
        html = f"<div class='a'>{PAGINATION_HTML}</div><div class='b'></div>"
        parser = parser_for(html)
        assert parser.try_parse_pagination(parser.try_get_tag("div.b")) is None
        assert parser.try_parse_pagination(parser.try_get_tag("div.a")).total_items == 177
