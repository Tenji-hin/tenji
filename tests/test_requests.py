from urllib.parse import parse_qs, urlparse

import pytest

from tenji.model.shop.shop_category import ShopCategory
from tenji.model.user.collectionstatus import CollectionStatus
from tenji.request.home import HomeRequest
from tenji.request.item.buy import BuyItemRequest
from tenji.request.item.item import ItemRequest
from tenji.request.login import LoginRequest
from tenji.request.request_base import RequestBase
from tenji.request.shop.shop import ShopRequest
from tenji.request.shop.shops import ShopsRequest
from tenji.request.user.collection import CollectionRequest
from tenji.request.user.profile import ProfileRequest
from tenji.request.user.user_list import UserListRequest
from tenji.request.user.users_lists import UserListsRequest

BASE_URL = "https://myfigurecollection.net/"


def query_of(url: str) -> dict:
    return {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}


class TestRequestBase:
    def test_unimplemented_methods_raise(self):
        req = RequestBase()
        with pytest.raises(NotImplementedError):
            req.get_path()
        with pytest.raises(NotImplementedError):
            req.get_method()

    def test_build_params_url_drops_none_values(self):
        url = RequestBase().build_params_url({"a": 1, "b": None, "c": "x y"})
        assert url == "a=1&c=x+y"

    def test_build_params_drops_none_values(self):
        params = RequestBase().build_params({"a": 1, "b": None})
        assert params == {"a": 1}

    def test_build_params_defaults_to_empty(self):
        assert RequestBase().build_params() == {}
        assert RequestBase().build_params_url() == ""

    def test_all_requests_use_the_mfc_base_url(self):
        requests = [
            HomeRequest(),
            LoginRequest("user", "pass"),
            ItemRequest(1),
            BuyItemRequest(1),
            ShopRequest(1),
            ShopsRequest(),
            CollectionRequest("user", CollectionStatus.Owned),
            ProfileRequest("user"),
            UserListRequest(1),
            UserListsRequest("user"),
        ]
        for req in requests:
            assert req.get_path().startswith(BASE_URL), type(req).__name__


class TestHomeRequest:
    def test_path_and_method(self):
        req = HomeRequest()
        assert req.get_path() == BASE_URL
        assert req.get_method() == "GET"


class TestLoginRequest:
    def test_path_and_method(self):
        req = LoginRequest("tester", "hunter2")
        assert req.get_path() == f"{BASE_URL}sessions.v4.php"
        assert req.get_method() == "POST"

    def test_params(self):
        params = LoginRequest("tester", "hunter2").get_params()
        assert params == {
            "username": "tester",
            "password": "hunter2",
            "commit": "signIn",
            "from": f"{BASE_URL}session/signin/",
        }


class TestItemRequest:
    def test_path_and_method(self):
        req = ItemRequest(198579)
        assert req.get_path() == f"{BASE_URL}item/198579"
        assert req.get_method() == "GET"


class TestBuyItemRequest:
    def test_path_and_method(self):
        req = BuyItemRequest(198579)
        assert req.get_path() == f"{BASE_URL}item/198579"
        assert req.get_method() == "POST"

    def test_default_params_omit_optional_values(self):
        assert BuyItemRequest(198579).get_params() == {
            "commit": "loadWindow",
            "window": "buyItem",
        }

    def test_user_listings_params(self):
        params = BuyItemRequest(198579, jan=4571245296795, users=True).get_params()
        assert params == {
            "commit": "loadWindow",
            "window": "buyItem",
            "soldBy": "users",
            "jan": 4571245296795,
        }


class TestShopRequest:
    def test_path_and_method(self):
        req = ShopRequest(153)
        assert req.get_path() == f"{BASE_URL}shop/153"
        assert req.get_method() == "GET"


class TestShopsRequest:
    def test_method(self):
        assert ShopsRequest().get_method() == "GET"

    def test_defaults_only_include_page(self):
        assert ShopsRequest().get_path() == f"{BASE_URL}shops.v4.php?page=1"

    def test_all_filters_are_encoded(self):
        req = ShopsRequest(
            keywords="good smile",
            location="JP",
            average_score=4,
            category=ShopCategory.WebShop,
            page=3,
        )
        path = req.get_path()
        assert path.startswith(f"{BASE_URL}shops.v4.php?")
        assert query_of(path) == {
            "keywords": "good smile",
            "location": "JP",
            "averageScore": "4",
            "categoryId": "1",
            "page": "3",
        }

    @pytest.mark.parametrize("category", list(ShopCategory))
    def test_category_is_serialised_as_its_value(self, category):
        # Formatting the enum member directly yields "ShopCategory.WebShop" on
        # Python 3.10 and below, so the value has to be used explicitly.
        query = query_of(ShopsRequest(category=category).get_path())
        assert query["categoryId"] == str(category.value)

    def test_category_accepts_a_plain_int(self):
        query = query_of(ShopsRequest(category=2).get_path())
        assert query["categoryId"] == "2"


class TestCollectionRequest:
    def test_method(self):
        assert CollectionRequest("tester", CollectionStatus.Owned).get_method() == "GET"

    @pytest.mark.parametrize(
        "status,expected",
        [
            (CollectionStatus.Wished, "0"),
            (CollectionStatus.Ordered, "1"),
            (CollectionStatus.Owned, "2"),
            (CollectionStatus.Favorites, "3"),
        ],
    )
    def test_status_is_serialised_as_its_value(self, status, expected):
        # Formatting the enum member directly yields "CollectionStatus.Owned" on
        # Python 3.11+, so the value has to be used explicitly.
        query = query_of(CollectionRequest("tester", status).get_path())
        assert query["status"] == expected

    def test_query_parameters(self):
        req = CollectionRequest("tester", CollectionStatus.Owned, page=4)
        query = query_of(req.get_path())
        assert query == {
            "mode": "view",
            "username": "tester",
            "tab": "collection",
            "page": "4",
            "status": "2",
            "output": "0",
        }

    def test_page_defaults_to_one(self):
        query = query_of(CollectionRequest("tester", CollectionStatus.Owned).get_path())
        assert query["page"] == "1"

    def test_status_accepts_a_plain_value(self):
        query = query_of(CollectionRequest("tester", 2).get_path())
        assert query["status"] == "2"


class TestProfileRequest:
    def test_path_and_method(self):
        req = ProfileRequest("tester")
        assert req.get_path() == f"{BASE_URL}profile/tester"
        assert req.get_method() == "GET"


class TestUserListRequest:
    def test_method(self):
        assert UserListRequest(1234).get_method() == "GET"

    def test_query_parameters(self):
        query = query_of(UserListRequest(1234, page=2).get_path())
        assert query == {
            "mode": "view",
            "itemListId": "1234",
            "tab": "view",
            "output": "0",
            "page": "2",
        }


class TestUserListsRequest:
    def test_method(self):
        assert UserListsRequest("tester").get_method() == "GET"

    def test_query_parameters(self):
        query = query_of(UserListsRequest("tester", page=3).get_path())
        assert query == {
            "mode": "view",
            "username": "tester",
            "tab": "lists",
            "page": "3",
        }
