from typing import Any, Optional
from bs4 import PageElement
from pydantic import BaseModel
from tenji.model.category import get_item_category_from_str
from tenji.model.item.item import Character, Company, Item
from tenji.parser.parser_base import ParserBase


class ItemParser(ParserBase):

    class ItemField(BaseModel):
        img: Optional[str] = None
        url: str
        name: str
        element: Optional[Any] = None

    def try_get_item_fields(self, labels: list[str]) -> list[ItemField]:
        fields = []
        for label in labels:
            container = self.get_item_field_container(label)
            if not container:
                continue

            field_links = container.select("a")

            for field_link in field_links:
                img_elem = field_link.select_one("img")
                img_url = img_elem.get("src") if img_elem else None
                url = field_link.get("href")
                name = field_link.select_one("span").text

                field = ItemParser.ItemField(img=img_url, url=url, name=name, element=field_link)
                fields.append(field)

        return fields

    def get_item_field_container(self, label: str) -> PageElement():
        label_node = self._soup.select_one(
            f"div.item-object div.form-label:-soup-contains('{label}')"
        )
        if label_node:
            return label_node.next_sibling
        return None

    def parse(self) -> Item:
        id = self.try_extract_number(self._soup.select_one("a.current").text)
        name = self._soup.select_one("span.h1-headline-value > span").text
        thumbnail = self._soup.select_one("span.h1-headline-icon > img").get("src")
        category = get_item_category_from_str(
            self.get_next_sibling_of("span.icon-tag").text
        )

        character_items = self.try_get_item_fields(["Character", "Characters"])
        characters = []
        for character_item in character_items:
            character = Character(
                id=self.try_extract_number(character_item.url),
                name=character_item.name,
                avatar=character_item.img,
            )
            characters.append(character)

        company_items = self.try_get_item_fields(["Company", "Companies"])
        companies = []
        for company_item in company_items:
            company = Company(
                id=self.try_extract_number(company_item.url),
                name=company_item.name,
                logo=company_item.img,
                role=company_item.element.select_one("small").text.replace("As ", "")
            )
            companies.append(company)

        item = Item(
            id=id,
            name=name,
            thumbnail=thumbnail,
            category=category,
            characters=characters,
            companies=companies
        )
        return item
