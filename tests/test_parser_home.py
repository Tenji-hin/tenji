from tenji.parser.home import HomeParser


class TestHomeParser:
    def test_signed_in_page(self, mfc_response):
        meta = HomeParser(mfc_response("home_user.html")).parse()
        assert meta.username == "tester"
        assert meta.avatar == "https://static.myfigurecollection.net/pics/avatar-42.jpg"
        # The sign-in control (span.icon-sliders) is only rendered for guests.
        assert meta.is_guest is False

    def test_guest_page(self, mfc_response):
        meta = HomeParser(mfc_response("home_guest.html")).parse()
        assert meta.is_guest is True
        assert meta.username is None
        assert meta.avatar is None
