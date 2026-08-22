import pytest

from tenji.mfc_response import MFCResponse
from tenji.model.shop.shop_category import ShopCategory
from tenji.parser.shop.shop import ShopParser
from tenji.parser.shop.shops import ShopsParser


class TestShopParser:
    @pytest.fixture
    def shop(self, mfc_response):
        return ShopParser(mfc_response("shop.html")).parse()

    def test_basic_fields(self, shop):
        assert shop.id == 153
        assert shop.name == "AmiAmi"
        assert shop.homepage == "https://www.amiami.com/"

    def test_location_and_shipping(self, shop):
        assert shop.location == "Japan"
        assert shop.shipping == "Ships worldwide"

    def test_contact_is_not_parsed_yet(self, shop):
        # The address is obfuscated by Cloudflare, so it is deliberately skipped.
        assert shop.contact is None

    def test_unknown_field_returns_none(self, mfc_response):
        parser = ShopParser(mfc_response("shop.html"))
        assert parser.get_shop_field_element("Opening hours") is None
        assert parser.get_shop_field_value("Opening hours") is None


class TestShopsParser:
    @pytest.fixture
    def shops(self, mfc_response):
        return ShopsParser(mfc_response("shops.html")).parse()

    def test_parses_every_result(self, shops):
        assert len(shops) == 2

    def test_fields(self, shops):
        assert [shop.id for shop in shops] == [153, 291]
        assert [shop.name for shop in shops] == ["AmiAmi", "Mandarake Nakano"]
        assert [shop.location for shop in shops] == ["Japan", "Tokyo, Japan"]
        assert (
            shops[0].icon
            == "https://static.myfigurecollection.net/pics/shop-153.png"
        )

    def test_categories(self, shops):
        assert shops[0].category is ShopCategory.WebShop
        assert shops[1].category is ShopCategory.LocalShop

    def test_no_results(self):
        html = "<div id='wide'><div><section><div class='results'></div></section></div></div>"
        assert ShopsParser(MFCResponse(html)).parse() == []
