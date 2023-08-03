from tenji.model.user.user_list_item import UserListItem
from tenji.model.user.users_lists import UserLists


from tenji.parser.parser_base import ParserBase


class UserListsParser(ParserBase):
    def parse(self) -> UserListItem:
        items = []

        results = self._soup.select("div.list-data")
        for result in results:
            link = result.select_one("div.list-anchor > a")
            name = link.text
            list_id = self.try_extract_number(link["href"])
            icon = result.select_one("img.list-icon")["src"]
            owner = result.select_one("div.list-meta > a").text

            creation_node = result.select_one("div.list-stats > span")
            created = self.try_parse_mfc_time(creation_node.get("title"))
            count = self.try_extract_number(creation_node.next_sibling.text)

            list = UserListItem(
                id=list_id,
                icon=icon,
                name=name,
                owner=owner,
                created=created,
                count=count,
            )

            items.append(list)

        pagination = self.try_parse_pagination()
        return UserLists(items=items, pagination=pagination)
