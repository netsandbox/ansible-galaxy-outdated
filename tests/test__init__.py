"""ansible-galaxy-outdated tests."""

from ansiblegalaxyoutdated import _display_collection, _get_collection_widths

TEST_COLLECTION = dict(name="Collection", version="Version", latest="Latest")


def test_get_collection_widths():
    """Test _get_collection_widths()."""
    assert _get_collection_widths([TEST_COLLECTION]) == (10, 7, 6)


def test_display_collection(capsys):
    """Test _display_collection()."""
    _display_collection(TEST_COLLECTION, 10, 7, 6)
    assert capsys.readouterr().out == "Collection Version Latest\n"

    _display_collection(TEST_COLLECTION, 11, 8, 7)
    assert capsys.readouterr().out == "Collection  Version  Latest \n"
