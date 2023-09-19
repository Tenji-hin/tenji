from bs4 import PageElement
from tenji.model.category import get_item_category_from_str
from tenji.model.item.item import Company, Item
from tenji.parser.parser_base import ParserBase


class ItemParser(ParserBase):

    def get_item_field_element(self, label: str) -> PageElement():
        label_node = self._soup.select_one(
            f"div.item-object div.form-label:-soup-contains('{label}')"
        )
        if label_node:
            return label_node.next_sibling
        return None

    def get_item_field_value(self, label: str) -> str:
        node = self.get_item_field_element(label)
        if node:
            return node.text
        return None

    def parse(self) -> Item:
        id = self.try_extract_number(self._soup.select_one("a.current").text)
        name = self._soup.select_one("span.h1-headline-value > span").text
        thumbnail = self._soup.select_one("span.h1-headline-icon > img").get("src")
        category = get_item_category_from_str(
            self.get_next_sibling_of("span.icon-tag").text
        )

        # company label is pluralized if there are multiple companies, so we need to check both
        company_elems = self.get_item_field_element("Company")
        if not company_elems:
            company_elems = self.get_item_field_element("Companies")

        companies = []

        for company_links in company_elems.select("a"):
            company_id = self.try_extract_number(company_links.get("href"))
            company_logo = company_links.select_one("img").get("src")
            company_name = company_links.select_one("span").text
            company_role = company_links.select_one("small").text.replace("As ", "")

            c = Company(id=company_id, name=company_name, logo=company_logo, role=company_role)
            companies.append(c)

        return Item(id=id, name=name, thumbnail=thumbnail, category=category, companies=companies)
