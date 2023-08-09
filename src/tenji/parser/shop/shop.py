from bs4 import PageElement
from tenji.model.shop.shop import Shop
from tenji.parser.parser_base import ParserBase


class ShopParser(ParserBase):
    def get_shop_field_element(self, label: str) -> PageElement():
        label_node = self._soup.select_one(
            f"div.shop-object div.form-label:-soup-contains('{label}')"
        )
        if label_node:
            return label_node.next_sibling
        return None

    def get_shop_field_value(self, label: str) -> str:
        node = self.get_shop_field_element(label)
        if node:
            return node.text
        return None

    def parse(self) -> Shop:
        name = self._soup.select_one("span.headline").text
        id = self.try_extract_number(self._soup.select_one("a.current").text)

        homepage = self.get_shop_field_value("Homepage")
        # TODO cloudflare email obfuscation
        contact = None  # self.get_shop_field_value("Contact")

        location_elem = self.get_shop_field_element("Location")
        location = self.try_get_text("span.shop-location", location_elem)
        shipping = self.try_get_text("small", location_elem)

        return Shop(
            id=id,
            name=name,
            homepage=homepage,
            contact=contact,
            location=location,
            shipping=shipping,
        )
