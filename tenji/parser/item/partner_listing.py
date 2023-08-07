from tenji.model.item import PartnerListing
from tenji.parser.parser_base import ParserBase


class PartnerItemListingParser(ParserBase):

    def parse(self) -> list[PartnerListing]:
        self.parse_html_from_json(self.response.body)

        listings = []
        
        results = self._soup.select("div.result")
        for result in results:
            stamp = result.select_one("div.stamp")
            link = stamp.select_one("a")
            icon = link.select_one("img")["src"]
            url = link["href"]

            jan = self.try_get_url_query_value(url, "jan")

            stamp_data = stamp.select_one("div.stamp-data")
            name = stamp_data.select_one("div.stamp-anchor").text

            availability = stamp_data.select_one("div.item-availability").text

            listing = PartnerListing(
                shop_icon=icon,
                shop_name=name,
                url=url,
                availability=availability,
                jan=jan,
                status=availability
            )

            listings.append(listing)

        return listings




        