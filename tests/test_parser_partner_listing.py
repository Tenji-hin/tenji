import json

import pytest

from tenji.mfc_response import MFCResponse
from tenji.model.item.partner_status import PartnerListingStatus
from tenji.parser.item.partner_listing import PartnerItemListingParser


@pytest.fixture
def listings(mfc_window_response):
    return PartnerItemListingParser(
        mfc_window_response("partner_listings.html")
    ).parse()


class TestPartnerItemListingParser:
    def test_parses_every_result(self, listings):
        assert len(listings) == 3

    def test_shop_details(self, listings):
        assert [listing.shop_name for listing in listings] == [
            "AmiAmi",
            "HobbySearch",
            "Good Smile Shop",
        ]
        assert (
            listings[0].shop_icon
            == "https://static.myfigurecollection.net/pics/shop-1.png"
        )

    def test_jan_is_taken_from_the_redirect_url(self, listings):
        assert [listing.jan for listing in listings] == [
            4571245296795,
            4573102620545,
            4580416941334,
        ]

    def test_statuses(self, listings):
        assert [listing.status for listing in listings] == [
            PartnerListingStatus.AVAILABLE,
            PartnerListingStatus.MAYBE_AVAILABLE,
            PartnerListingStatus.NOT_AVAILABLE,
        ]

    def test_url_entities_are_decoded(self, listings):
        assert listings[0].url == (
            "https://myfigurecollection.net/redirect.php?shop=1&jan=4571245296795"
        )

    def test_empty_window_yields_no_listings(self):
        body = json.dumps({"htmlValues": {"WINDOW": "<div class='results'></div>"}})
        assert PartnerItemListingParser(MFCResponse(body)).parse() == []
