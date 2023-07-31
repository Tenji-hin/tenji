from tenji.model.shop.shop_category import ShopCategory
from tenji.request import RequestBase


class ShopsRequest(RequestBase):
    def __init__(
        self,
        keywords: str = None,
        location: str = None,
        average_score: int = None,
        category: ShopCategory = None,
        page: int = 1,
    ) -> None:
        self.keywords = keywords
        self.location = location
        self.average_score = average_score
        self.category = category
        self.page = page

    def getPath(self) -> str:
        path = f"{self.BASE_URL}shops.v4.php"

        params = {
            "keywords": self.keywords,
            "location": self.location,
            "averageScore": self.average_score,
            "categoryId": self.category,
            "page": self.page,
        }

        return f"{path}?{self.build_params_url(params)}"

    def getMethod(self):
        return "GET"
