from http.cookies import SimpleCookie
from typing import Optional
from tenji.exceptions import *
from tenji.mfc_response import MFCResponse
from tenji.model import *
from tenji.parser import *
from tenji.request import *
from yarl import URL
import aiohttp
import logging

from tenji.request.request_base import RequestBase

class MFCException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class MfcClient:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    LOGIN_FAILURE_TEXT = "Sorry, check your username and password"

    def __init__(self, session_id: str = None) -> None:
        self._session_id = session_id
        self._session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(__name__)

    @property
    def session(self) -> aiohttp.ClientSession:
        """The underlying HTTP session, opened on first use.

        It is created lazily so that constructing a client outside of a running
        event loop is safe, as aiohttp expects its session to be created from a
        coroutine.
        """
        if self._session is None:
            cookies = {}
            if self._session_id:
                cookies["PHPSESSID"] = self._session_id

            self._session = aiohttp.ClientSession(
                headers={"User-Agent": self.USER_AGENT}, cookies=cookies
            )
        return self._session

    async def __aenter__(self) -> "MfcClient":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()

    async def close(self) -> None:
        """Closes the underlying HTTP session and releases its connections"""
        if self._session is not None and not self._session.closed:
            await self._session.close()

    def set_session(self, session: aiohttp.ClientSession):
        self._session = session

    async def is_logged_in(self) -> tuple[bool, Optional[str]]:
        """Returns a tuple of whether the client is logged in and the username"""
        req = HomeRequest()
        res = await self.__perform_modeled_request(req)
        parser = HomeParser(res)
        meta = parser.parse()
        return (not meta.is_guest, meta.username)

    async def login(self, username: str, password: str) -> tuple[bool, SimpleCookie]:
        """Logs in to MFC using the given username and password"""

        req = LoginRequest(username, password)
        res = await self.__perform_modeled_request(req)
        success = self.LOGIN_FAILURE_TEXT not in res.soup.text
        # aiohttp files any Set-Cookie header into the session jar for us
        cookies = self.session.cookie_jar.filter_cookies(URL(RequestBase.BASE_URL))
        return (success, cookies)

    async def logout(self) -> bool:
        url = "https://myfigurecollection.net/session/signout/"

        async with self.session.get(url) as response:
            if response.status != 200:
                raise Exception("Failed to perform request")
            html = await response.text()

        # TODO check if logout was successful

        return True

    async def get_profile(self, username: str) -> Profile:
        """Returns a Profile object for the given username"""
        req = ProfileRequest(username)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ProfileParser(res)
            profile = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e
        return profile

    async def get_collection(
        self, username: str, status: Collection, page: int = 1
    ) -> Collection:
        """Returns a Collection object for the given username and status"""
        req = CollectionRequest(username, status, page)
        res = await self.__perform_modeled_request(req)
        try:
            parser = CollectionParser(res)
            collection = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e
        return collection

    async def get_lists(self, username: str) -> UserLists:
        """Gets public lists for a given user"""
        req = UserListsRequest(username)
        res = await self.__perform_modeled_request(req)
        try:
            parser = UserListsParser(res)
            lists = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e
        return lists

    async def get_item(self, id: int) -> Item:
        """Returns an Item object for the given id"""
        req = ItemRequest(id)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ItemParser(res)
            item = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e

        return item

    async def get_list(self, id: int, page: int = 1) -> UserList:
        """Returns a List object for the given id"""
        req = UserListRequest(id, page)
        res = await self.__perform_modeled_request(req)
        try:
            parser = UserListParser(res)
            list = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e

        return list

    async def get_partner_listings(self, item_id: int) -> list[PartnerListing]:
        """Returns item availabilities from partners"""
        req = BuyItemRequest(item_id)
        res = await self.__perform_modeled_request(req)
        
        try:
            parser = PartnerItemListingParser(res)
            listings = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e
        return listings

    async def get_shop(self, id: int) -> Shop:
        """Returns a Shop object for the given id"""
        req = ShopRequest(id)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ShopParser(res)
            shop = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e
        return shop

    async def get_shops(
        self,
        keywords: str = None,
        location: str = None,
        average_score: int = None,
        category: str = None,
        page: int = 1,
    ) -> list[ShopListItem]:
        """Returns a list of Shops"""
        req = ShopsRequest(keywords, location, average_score, category, page)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ShopsParser(res)
            shop = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e) from e
        return shop

    async def __perform_modeled_request(self, req: RequestBase) -> MFCResponse:
        """Performs a request and returns the response"""

        method = req.get_method()
        if method == "GET":
            request = self.session.get(req.get_path())
        elif method == "POST":
            request = self.session.post(req.get_path(), data=req.get_params())
        else:
            raise RequestException(
                f"Unsupported request method {method!r} for {req.get_path()}"
            )

        async with request as response:
            if response.status != 200:
                raise RequestException(
                    f"Failed to perform request: {req.get_path()} "
                    f"returned HTTP {response.status}"
                )
            response_body = await response.text()

        return MFCResponse(response_body)
