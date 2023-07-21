from bs4 import BeautifulSoup
from mfc.model.profile import About, Profile
from mfc.parser import ParserBase


class ProfileParser(ParserBase):
    def parse(self) -> Profile:
        username = self._soup.select_one("span.h1-headline-value > span.headline").text

        subtitle_node = self._soup.select_one("span.h1-headline-value > span.subtitle")
        subtitle = subtitle_node.text if subtitle_node else None

        status_node = self._soup.select_one("span.tbx-target-STATUS")
        status = status_node.text if status_node else None

        avatar = self._soup.select_one("img.the-avatar").get("src")
        stats_container = self._soup.select_one("div.object-stats")
        online_status = stats_container.select_one("span:nth-child(1)").text
        joined = stats_container.select_one("span:nth-child(2)").text
        hits = stats_container.contents[6].text
        rank = None

        about_container = self._soup.select_one("div.data_2")

        level = self.try_get_text(
            "div.form-label:contains('Level') + div > a", about_container
        )
        gender = self.try_get_text(
            "div.form-label:contains('Gender') + div > a", about_container
        )
        age = self.try_get_text("div.form-label:contains('Age') + div", about_container)
        location = self.try_get_text(
            "div.form-label:contains('Location') + div", about_container
        )
        occupation = self.try_get_text(
            "div.form-label:contains('Occupation') + div", about_container
        )
        homepage = self.try_get_text(
            "div.form-label:contains('Homepage') + div > a", about_container
        )
        shows = self.try_get_list(
            "div.form-label:contains('Shows(s)') + div > a", about_container, []
        )
        games = self.try_get_list(
            "div.form-label:contains('Game(s)') + div", about_container, []
        )
        moe_points = self.try_get_list(
            "div.form-label:contains('MOE Point(s)') + div", about_container, []
        )

        about = About(
            level=level,
            gender=gender,
            age=age,
            location=location,
            occupation=occupation,
            homepage=homepage,
            shows=shows,
            games=games,
            moe_points=moe_points,
        )

        return Profile(
            username=username,
            subtitle=subtitle,
            status=status,
            avatar=avatar,
            online_status=online_status,
            joined=joined,
            hits=hits,
            rank=rank,
            about=about,
        )
