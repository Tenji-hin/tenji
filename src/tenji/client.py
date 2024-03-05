from http.cookies import SimpleCookie
from tenji.exceptions import *
from tenji.mfc_response import MFCResponse
from tenji.model import *
from tenji.parser import *
from tenji.request import *
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
        parser = HomeParser(res)
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
            parser = ProfileParser(res)
            profile = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
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
            raise ParserException.from_request(req, e)
        return collection

    async def get_lists(self, username: str) -> UserLists:
        """Gets public lists for a given user"""
        req = UserListsRequest(username)
        res = await self.__perform_modeled_request(req)
        try:
            parser = UserListsParser(res)
            lists = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
        return lists

    async def get_item(self, id: int) -> Item:
        """Returns an Item object for the given id"""
        req = ItemRequest(id)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ItemParser(res)
            item = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)

        return item

    async def get_list(self, id: int, page: int = 1) -> UserList:
        """Returns a List object for the given id"""
        req = UserListRequest(id, page)
        res = await self.__perform_modeled_request(req)
        try:
            parser = UserListParser(res)
            list = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)

        return list

    async def get_partner_listings(self, item_id: int) -> list[PartnerListing]:
        """Returns item availabilities from partners"""
        req = BuyItemRequest(item_id)
        res = await self.__perform_modeled_request(req)
        
        try:
            parser = PartnerItemListingParser(res)
            listings = parser.parse()
        except Exception as e:
            raise ParserException.from_request(req, e)
        return listings

    async def get_shop(self, id: int) -> Shop:
        """Returns a Shop object for the given id"""
        req = ShopRequest(id)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ShopParser(res)
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
            parser = ShopsParser(res)
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
                    raise RequestException(f"Failed to perform request: {req.getPath()}")
                response_body = await response.text()
        elif method == "POST":
            async with self._session.post(
                req.getPath(), data=req.getParams()
            ) as response:
                if response.status != 200:
                    raise RequestException(f"Failed to perform request {req.getPath()}")
                response_body = await response.text()
  
        res = MFCResponse(response_body)
        return res
