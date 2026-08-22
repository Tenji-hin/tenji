import asyncio
import json

from http.cookies import SimpleCookie

import pytest
from yarl import URL

from tenji.client import MfcClient
from tenji.exceptions.parser_exception import ParserException
from tenji.exceptions.request_exception import RequestException
from tenji.model.category import ItemCategory
from tenji.model.user.collectionstatus import CollectionStatus

from conftest import read_fixture

MFC_URL = "https://myfigurecollection.net/"


class FakeResponse:
    def __init__(self, body: str, status: int = 200) -> None:
        self._body = body
        self.status = status

    async def text(self) -> str:
        return self._body


class FakeRequestContext:
    def __init__(self, response: FakeResponse) -> None:
        self._response = response

    async def __aenter__(self) -> FakeResponse:
        return self._response

    async def __aexit__(self, *args) -> bool:
        return False


class FakeCookieJar:
    """Stands in for aiohttp.CookieJar, which cannot be built outside a loop."""

    def __init__(self, cookies: dict = None) -> None:
        self._cookies = SimpleCookie()
        for name, value in (cookies or {}).items():
            self._cookies[name] = value
        self.filtered_urls = []

    def filter_cookies(self, url) -> SimpleCookie:
        self.filtered_urls.append(url)
        return self._cookies


class FakeSession:
    """Stands in for aiohttp.ClientSession and records the calls made to it."""

    def __init__(self, body: str = "", status: int = 200, cookies: dict = None) -> None:
        self.response = FakeResponse(body, status)
        self.calls = []
        self.closed = False
        self.cookie_jar = FakeCookieJar(cookies)

    async def close(self):
        self.closed = True

    def get(self, url, **kwargs):
        self.calls.append(("GET", url, kwargs.get("data")))
        return FakeRequestContext(self.response)

    def post(self, url, data=None, **kwargs):
        self.calls.append(("POST", url, data))
        return FakeRequestContext(self.response)

    @property
    def last_call(self):
        return self.calls[-1]


def run_with_session(session: FakeSession, call):
    """Runs `call(client)` against a client backed by the given fake session."""

    async def main():
        client = MfcClient()
        client.set_session(session)
        return await call(client)

    return asyncio.run(main())


class TestClientRequests:
    def test_get_item_requests_and_parses_the_item(self):
        session = FakeSession(read_fixture("item.html"))
        item = run_with_session(session, lambda c: c.get_item(198579))

        assert session.last_call == ("GET", "https://myfigurecollection.net/item/198579", None)
        assert item.id == 198579
        assert item.category is ItemCategory.Prepainted

    def test_get_profile(self):
        session = FakeSession(read_fixture("profile.html"))
        profile = run_with_session(session, lambda c: c.get_profile("tester"))

        assert session.last_call[1] == "https://myfigurecollection.net/profile/tester"
        assert profile.username == "tester"

    def test_get_collection_passes_the_status_and_page(self):
        session = FakeSession(read_fixture("collection.html"))
        collection = run_with_session(
            session,
            lambda c: c.get_collection("tester", CollectionStatus.Owned, page=2),
        )

        url = session.last_call[1]
        assert "username=tester" in url
        assert "status=2" in url
        assert "page=2" in url
        assert len(collection.items) == 3

    def test_get_lists(self):
        session = FakeSession(read_fixture("user_lists.html"))
        lists = run_with_session(session, lambda c: c.get_lists("tester"))

        assert "tab=lists" in session.last_call[1]
        assert len(lists.items) == 2

    def test_get_list(self):
        session = FakeSession(read_fixture("user_list.html"))
        user_list = run_with_session(session, lambda c: c.get_list(1234))

        assert "itemListId=1234" in session.last_call[1]
        assert user_list.name == "Favourite Mikus"

    def test_get_shop(self):
        session = FakeSession(read_fixture("shop.html"))
        shop = run_with_session(session, lambda c: c.get_shop(153))

        assert session.last_call[1] == "https://myfigurecollection.net/shop/153"
        assert shop.name == "AmiAmi"

    def test_get_shops(self):
        session = FakeSession(read_fixture("shops.html"))
        shops = run_with_session(session, lambda c: c.get_shops(keywords="ami"))

        assert "keywords=ami" in session.last_call[1]
        assert len(shops) == 2

    def test_get_partner_listings_uses_a_post_request(self):
        body = json.dumps(
            {"htmlValues": {"WINDOW": read_fixture("partner_listings.html")}}
        )
        session = FakeSession(body)
        listings = run_with_session(session, lambda c: c.get_partner_listings(198579))

        method, url, data = session.last_call
        assert method == "POST"
        assert url == "https://myfigurecollection.net/item/198579"
        assert data == {"commit": "loadWindow", "window": "buyItem"}
        assert len(listings) == 3


class TestAuthentication:
    def test_is_logged_in_is_true_for_a_signed_in_page(self):
        session = FakeSession(read_fixture("home_user.html"))
        logged_in, username = run_with_session(session, lambda c: c.is_logged_in())

        assert session.last_call[1] == MFC_URL
        assert logged_in is True
        assert username == "tester"

    def test_is_logged_in_is_false_for_a_guest_page(self):
        session = FakeSession(read_fixture("home_guest.html"))
        logged_in, username = run_with_session(session, lambda c: c.is_logged_in())

        assert logged_in is False
        assert username is None

    def test_login_posts_the_credentials(self):
        session = FakeSession(read_fixture("home_user.html"))
        run_with_session(session, lambda c: c.login("tester", "hunter2"))

        method, url, data = session.last_call
        assert method == "POST"
        assert url == f"{MFC_URL}sessions.v4.php"
        assert data["username"] == "tester"
        assert data["password"] == "hunter2"
        assert data["commit"] == "signIn"

    def test_login_succeeds_and_returns_the_session_cookies(self):
        session = FakeSession(
            read_fixture("home_user.html"), cookies={"PHPSESSID": "abc123"}
        )
        success, cookies = run_with_session(
            session, lambda c: c.login("tester", "hunter2")
        )

        assert success is True
        assert cookies["PHPSESSID"].value == "abc123"

    def test_login_filters_cookies_with_a_url_instance(self):
        # aiohttp 4.x drops support for passing a plain string here
        session = FakeSession(read_fixture("home_user.html"))
        run_with_session(session, lambda c: c.login("tester", "hunter2"))

        assert session.cookie_jar.filtered_urls == [URL("https://myfigurecollection.net/")]

    def test_login_detects_a_rejected_password(self):
        session = FakeSession(read_fixture("login_failed.html"))
        success, _ = run_with_session(session, lambda c: c.login("tester", "wrong"))

        assert success is False


class TestClientErrors:
    def test_non_200_responses_raise_a_request_exception(self):
        session = FakeSession("", status=500)
        with pytest.raises(RequestException):
            run_with_session(session, lambda c: c.get_item(198579))

    def test_unparseable_bodies_raise_a_parser_exception(self):
        session = FakeSession("<html><body>maintenance</body></html>")
        with pytest.raises(ParserException):
            run_with_session(session, lambda c: c.get_item(198579))

    def test_parser_failures_are_wrapped_for_every_endpoint(self):
        broken = "<html><body>maintenance</body></html>"
        calls = [
            lambda c: c.get_profile("tester"),
            lambda c: c.get_collection("tester", CollectionStatus.Owned),
            lambda c: c.get_lists("tester"),
            lambda c: c.get_list(1234),
            lambda c: c.get_shop(153),
        ]
        for call in calls:
            with pytest.raises(ParserException):
                run_with_session(FakeSession(broken), call)


class TestClientSession:
    def test_constructing_a_client_opens_no_session(self):
        # aiohttp wants its session created from a coroutine, so building a
        # client outside of a running loop must not touch the network stack
        client = MfcClient()
        assert client._session is None

    def test_the_session_is_created_on_first_access(self):
        async def main():
            client = MfcClient()
            try:
                session = client.session
                assert client.session is session
                return session
            finally:
                await client.close()

        assert asyncio.run(main()) is not None

    def test_session_id_is_sent_as_a_cookie(self):
        async def main():
            client = MfcClient(session_id="abc123")
            try:
                cookies = client.session.cookie_jar.filter_cookies(
                    URL("https://myfigurecollection.net")
                )
                return cookies["PHPSESSID"].value
            finally:
                await client.close()

        assert asyncio.run(main()) == "abc123"

    def test_user_agent_header_is_set(self):
        async def main():
            client = MfcClient()
            try:
                return client.session.headers["User-Agent"]
            finally:
                await client.close()

        assert "Mozilla/5.0" in asyncio.run(main())

    def test_close_closes_the_session(self):
        session = FakeSession()

        async def main():
            client = MfcClient()
            client.set_session(session)
            await client.close()

        asyncio.run(main())
        assert session.closed is True

    def test_close_is_a_no_op_when_no_session_was_opened(self):
        async def main():
            client = MfcClient()
            await client.close()
            return client._session

        assert asyncio.run(main()) is None

    def test_close_is_idempotent(self):
        async def main():
            client = MfcClient()
            client.session  # force the session open
            await client.close()
            await client.close()
            return client._session.closed

        assert asyncio.run(main()) is True

    def test_async_context_manager_closes_the_session(self):
        session = FakeSession(read_fixture("item.html"))

        async def main():
            client = MfcClient()
            client.set_session(session)
            async with client as entered:
                assert entered is client
                await entered.get_item(198579)

        asyncio.run(main())
        assert session.closed is True
