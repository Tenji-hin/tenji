"""Guards the public API surface consumers see after `pip install tenji`."""

import importlib.resources

import pytest

import tenji


class TestPublicApi:
    def test_version_is_exposed(self):
        assert isinstance(tenji.__version__, str)
        assert tenji.__version__

    @pytest.mark.parametrize("name", sorted(tenji.__all__))
    def test_everything_in_all_is_importable(self, name):
        assert hasattr(tenji, name), f"tenji.__all__ advertises missing {name!r}"

    def test_star_import_matches_all(self):
        namespace = {}
        exec("from tenji import *", namespace)
        exported = {k for k in namespace if not k.startswith("__")}
        assert exported == set(tenji.__all__) - {"__version__"}

    def test_client_is_the_documented_entry_point(self):
        from tenji import MfcClient

        assert MfcClient is tenji.MfcClient

    @pytest.mark.parametrize(
        "name",
        [
            "CollectionStatus",
            "ItemCategory",
            "ShopCategory",
            "Item",
            "Profile",
            "Collection",
            "UserList",
            "Shop",
            "ParserException",
            "RequestException",
        ],
    )
    def test_types_needed_to_call_the_client_are_top_level(self, name):
        # these are arguments to or return values from MfcClient methods, so
        # consumers must not have to reach into tenji.model.* for them
        assert hasattr(tenji, name)


class TestTypingSupport:
    def test_py_typed_marker_ships_with_the_package(self):
        package_dir = importlib.resources.files("tenji")
        assert (package_dir / "py.typed").is_file()
