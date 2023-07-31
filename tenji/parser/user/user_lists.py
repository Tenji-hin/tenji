from tenji.model.paginated import Pagination
from tenji.model.user.user_list_item import UserListItem

from tenji.model.user.users_lists import UserLists
from tenji.parser import ParserBase


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
            created = result.select_one("div.list-stats > span").get("title")

            creation_node = result.select_one("div.list-stats > span")
            created = creation_node.get("title")
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

        pagination_controls = self._soup.select_one("div.results-count-pages")

        if pagination_controls is None:
            return UserLists(items=items)

        current_link = pagination_controls.select_one("a.nav-current")
        next_link = pagination_controls.select_one("a.nav-next")

        pagination = Pagination(
            current_page=self.try_extract_number(current_link.text),
            has_next_page=next_link is not None,
        )

        return UserLists(items=items, pagination=pagination)
