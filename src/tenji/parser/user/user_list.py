from tenji.model.category import get_item_category_from_str
from tenji.model.item.item import Item

from tenji.model.user.user_list import UserList
from tenji.parser.parser_base import ParserBase


class UserListParser(ParserBase):
    def parse(self) -> UserList:
        items = []

        icon = self._soup.select_one("span.h1-headline-icon > img").get("src")
        name = self._soup.select_one("span.h1-headline-value > span").text

        list_id = self.try_extract_number(self._soup.select_one("a.current").text)

        list_info_container = self._soup.select_one("div.itemlist-object")

        owner = list_info_container.select_one("a.user-anchor").text

        description = list_info_container.select_one("div.bbcode").decode_contents()
        created = self.try_parse_mfc_time(
            list_info_container.select_one("span.time > span:nth-child(2)").get("title")
        )

        item_stamps = self._soup.select("div.item-stamp")
        for item_stamp in item_stamps:
            link = item_stamp.select_one("a")
            item_id = self.try_extract_number(link.get("href"))
            item_thumbnail = link.select_one("img").get("src")
            item_name = link.select_one("img").get("alt")
            item_category = get_item_category_from_str(
                item_stamp.select_one("div.stamp-category").text
            )

            item = Item(
                id=item_id,
                name=item_name,
                thumbnail=item_thumbnail,
                category=item_category,
            )

            items.append(item)

        tags = []
        tag_nodes = self._soup.select("div.object-tag")
        for tag_node in tag_nodes:
            tag = tag_node.select_one("a").text
            tags.append(tag)

        pagination = self.try_parse_pagination()

        return UserList(
            id=list_id,
            name=name,
            owner=owner,
            icon=icon,
            created=created,
            description=description,
            items=items,
            tags=tags,
            pagination=pagination,
        )
