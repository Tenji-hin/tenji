from mfc.model.meta import Meta
from mfc.parser import ParserBase


class HomeParser(ParserBase):
    def parse(self) -> Meta:
        user_menu = self._soup.select_one("div.user-menu")

        handle_link = user_menu.select_one("a.handle")

        is_guest = True

        notif_count = None  # anything greater than 9 will show as 9+
        username = None
        avatar = None

        if self._soup.select_one("span.icon-sliders") is None:
            is_guest = False

        if handle_link:
            notif_count = self.try_get_text("span.count", user_menu, None)
            username = self.try_get_text("span.username", handle_link)
            avatar = self.try_get_value("img", "src", handle_link)

        return Meta(is_guest=is_guest, username=username, avatar=avatar)
