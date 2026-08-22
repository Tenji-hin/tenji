from tenji.model.shop.shop_category import ShopCategory
from tenji.request.request_base import RequestBase


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

    def get_path(self) -> str:
        path = f"{self.BASE_URL}shops.v4.php"

        params = {
            "keywords": self.keywords,
            "location": self.location,
            "averageScore": self.average_score,
            # int() so the enum is encoded as its value on every Python version
            "categoryId": int(self.category) if self.category is not None else None,
            "page": self.page,
        }

        return f"{path}?{self.build_params_url(params)}"

    def get_method(self):
        return "GET"
