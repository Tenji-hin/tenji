from http.cookies import SimpleCookie
from bs4 import BeautifulSoup
from tenji.exceptions.parser_exception import ParserException
from tenji.model.shop.shop import Shop
from tenji.model.shop.shop_list_item import ShopListItem
from tenji.model.user.collection import Collection
from tenji.model.item.item import Item
from tenji.model.user.user_list import UserList
from tenji.model.user.users_lists import UserLists
from tenji.parser.shop.shop import ShopParser
from tenji.parser.shop.shops import ShopsParser
from tenji.parser.user.collection import CollectionParser
from tenji.parser.home import HomeParser
from tenji.parser.item.item import ItemParser
from tenji.parser.user.user_list import UserListParser
from tenji.parser.user.profile import ProfileParser
from tenji.parser.user.user_lists import UserListsParser
from tenji.request import RequestBase
from tenji.request.shop.shop import ShopRequest
from tenji.request.shop.shops import ShopsRequest
from tenji.request.user.collection import CollectionRequest, CollectionStatus
from tenji.request.home import HomeRequest
from tenji.request.item.item import ItemRequest
from tenji.request.user.user_list import UserListRequest
from tenji.request.user.users_lists import UserListsRequest
from tenji.request.login import LoginRequest

from tenji.request.user.profile import ProfileRequest
from .model.user.profile import Profile
import aiohttp
import logging


class MFCResponse:
    def __init__(self, response: aiohttp.ClientResponse, soup: BeautifulSoup) -> None:
        self.response = response
        self.soup = soup


class MFCException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class MfcClient:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

    def __init__(self, session_id: str = None) -> None:
        cookies = {}
        if session_id:
            cookies["PHPSESSID"] = session_id

        self._session = aiohttp.ClientSession(
            headers={"User-Agent": self.USER_AGENT}, cookies=cookies
        )
        self.logger = logging.getLogger(__name__)

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()

    def set_session(self, session: aiohttp.ClientSession):
        self._session = session

    async def is_logged_in(self) -> tuple[bool, str]:
        """Returns a tuple of whether the client is logged in and the username"""
        req = HomeRequest()
        res = await self.__perform_modeled_request(req)
        parser = HomeParser(res.soup)
        meta = parser.parse()
        return (meta.is_guest, meta.username)

    async def login(self, username: str, password: str) -> tuple[bool, SimpleCookie]:
        """Logs in to MFC using the given username and password"""

        req = LoginRequest(username, password)
        response = await self.__perform_modeled_request(req)
        success = "Sorry, check your username and password" not in response.soup.text
        cookies = response.response.cookies
        if cookies:
            self._session.cookie_jar.update_cookies(cookies)
        filtered = self._session.cookie_jar.filter_cookies(
            "https://myfigurecollection.net"
        )
        return (success, filtered)

    async def logout(self) -> bool:
        url = "https://myfigurecollection.net/session/signout/"

        async with self._session.get(url) as response:
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
            parser = ProfileParser(res.soup)
            profile = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
        return profile

    async def get_collection(
        self, username: str, status: CollectionStatus, page: int = 1
    ) -> Collection:
        """Returns a Collection object for the given username and status"""
        req = CollectionRequest(username, status, page)
        res = await self.__perform_modeled_request(req)
        try:
            parser = CollectionParser(res.soup)
            collection = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
        return collection

    async def get_lists(self, username: str) -> UserLists:
        """Gets public lists for a given user"""
        req = UserListsRequest(username)
        res = await self.__perform_modeled_request(req)
        try:
            parser = UserListsParser(res.soup)
            lists = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
        return lists

    async def get_item(self, id: int) -> Item:
        """Returns an Item object for the given id"""
        req = ItemRequest(id)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ItemParser(res.soup)
            item = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)

        return item

    async def get_list(self, id: int, page: int = 1) -> UserList:
        """Returns a List object for the given id"""
        req = UserListRequest(id, page)
        res = await self.__perform_modeled_request(req)
        try:
            parser = UserListParser(res.soup)
            list = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)

        return list

    async def get_shop(self, id: int) -> Shop:
        """Returns a Shop object for the given id"""
        req = ShopRequest(id)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ShopParser(res.soup)
            shop = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
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
            parser = ShopsParser(res.soup)
            shop = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
        return shop

    async def __perform_modeled_request(self, req: RequestBase) -> MFCResponse:
        """Performs a request and returns the response"""

        method = req.getMethod()
        if method == "GET":
            async with self._session.get(req.getPath()) as response:
                if response.status != 200:
                    raise Exception("Failed to perform request")
                response_body = await response.text()
        elif method == "POST":
            async with self._session.post(
                req.getPath(), data=req.getParams()
            ) as response:
                if response.status != 200:
                    raise Exception("Failed to perform request")
                response_body = await response.text()

        soup = BeautifulSoup(response_body, "html.parser")

        res = MFCResponse(response, soup)
        return res
