from bs4 import BeautifulSoup
from mfc.exceptions.parser_exception import ParserException
from mfc.parser.profile import ProfileParser
from mfc.request import RequestBase

from mfc.request.profile import ProfileRequest
from .model.profile import Profile
import aiohttp
import logging


class MfcClient:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()
        self.logger = logging.getLogger(__name__)

    def __exit__(self, exc_type, exc_value, traceback):
        self._session.close()

    async def get_profile(self, username: str) -> Profile:
        """Returns a Profile object for the given username"""
        req = ProfileRequest(username)
        soup = await self.__perform_request(req)
        try:
            parser = ProfileParser(soup)
            profile = parser.parse()
        except Exception as e:
            self.logger.error(f"Failed to parse profile: {e}")
            raise ParserException("Failed to parse profile")
        return profile

    async def __perform_request(self, req: RequestBase) -> BeautifulSoup:
        """Performs a request and returns the response as a BeautifulSoup object"""

        async with self._session.get(req.getPath()) as response:
            if response.status != 200:
                raise Exception("Failed to perform request")
            html = await response.text()

        soup = BeautifulSoup(html, "html.parser")
        return soup
