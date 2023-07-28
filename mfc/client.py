from http.cookies import Morsel, SimpleCookie
from bs4 import BeautifulSoup
from mfc.exceptions.parser_exception import ParserException
from mfc.model.collection import Collection
from mfc.model.item import Item
from mfc.parser.collection import CollectionParser
from mfc.parser.home import HomeParser
from mfc.parser.item import ItemParser
from mfc.parser.profile import ProfileParser
from mfc.request import RequestBase
from mfc.request.collection import CollectionRequest, CollectionStatus
from mfc.request.home import HomeRequest
from mfc.request.item import ItemRequest
from mfc.request.login import LoginRequest

from mfc.request.profile import ProfileRequest
from .model.profile import Profile
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
            self.logger.error(f"Failed to parse profile: {e}")
            raise ParserException("Failed to parse profile")
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
            self.logger.error(f"Failed to parse collection: {e}")
            raise ParserException("Failed to parse collection")
        return collection

    async def get_item(self, id: int) -> Item:
        """Returns an Item object for the given id"""
        req = ItemRequest(id)
        res = await self.__perform_modeled_request(req)
        try:
            parser = ItemParser(res.soup)
            item = parser.parse()
        except Exception as e:
            self.logger.error(f"Failed to parse item: {e}")
            raise ParserException("Failed to parse item")

        return item

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
