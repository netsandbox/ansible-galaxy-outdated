"""ansible-galaxy-outdated."""

import json
import os
import subprocess
import sys
import urllib.request

HEADER = dict(name="Collection", version="Version", latest="Latest")


def _get_collection_widths(collections):
    name_set = {c["name"] for c in collections}
    version_set = {c["version"] for c in collections}
    latest_set = {c["latest"] for c in collections}

    name_length = len(max(name_set, key=len))
    version_length = len(max(version_set, key=len))
    latest_length = len(max(latest_set, key=len))

    return name_length, version_length, latest_length


def _display_collection(collection, name_width, version_width, latest_width):
    min_name_width = len(HEADER["name"])
    min_version_width = len(HEADER["version"])
    min_latest_width = len(HEADER["latest"])

    print(
        (
            f"{collection['name']:{max(name_width, min_name_width)}} "
            f"{collection['version']:{max(version_width, min_version_width)}} "
            f"{collection['latest']:{max(latest_width, min_latest_width)}}"
        )
    )


def _get_latest_version(collection_name):
    url = f"https://galaxy.ansible.com/api/v2/collections/{collection_name.replace('.', '/')}/"

    with urllib.request.urlopen(url) as f:
        galaxy_data = json.load(f)

    if galaxy_data["deprecated"]:
        print(f"WARNING: collection {collection_name} is deprecated")

    return galaxy_data["latest_version"]["version"]


def _running_under_venv():
    """Check if sys.base_prefix and sys.prefix match.

    This handles PEP 405 compliant virtual environments.
    """
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def _running_under_legacy_virtualenv():
    """Check if sys.real_prefix is set.

    This handles virtual environments created with pypa's virtualenv.
    """
    return hasattr(sys, "real_prefix")


def main():
    """Run main function."""
    if _running_under_venv() or _running_under_legacy_virtualenv():
        prefix = os.path.normpath(sys.prefix)
        ansible_galaxy_bin = os.path.join(prefix, "bin", "ansible-galaxy")
    else:
        ansible_galaxy_bin = "ansible-galaxy"

    try:
        collections_json = subprocess.check_output([ansible_galaxy_bin, "collection", "list", "--format=json"])
    except FileNotFoundError:
        sys.exit("ansible-galaxy not found")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ansible-galaxy error: {e}")

    collections = json.loads(collections_json)
    collections = collections[list(collections.keys())[0]]

    data = []
    for collection_name, collection_data in sorted(collections.items()):
        latest = _get_latest_version(collection_name)
        if collection_data["version"] != latest:
            data.append(dict(name=collection_name, version=collection_data["version"], latest=latest))

    if not data:
        return 0

    name_width, version_width, latest_width = _get_collection_widths(data)

    _display_collection(HEADER, name_width, version_width, latest_width)

    separator = dict(
        name="-" * max(name_width, len(HEADER["name"])),
        version="-" * max(version_width, len(HEADER["version"])),
        latest="-" * max(latest_width, len(HEADER["latest"])),
    )
    _display_collection(separator, name_width, version_width, latest_width)

    for collection in data:
        _display_collection(collection, name_width, version_width, latest_width)

    return 0


if __name__ == "__main__":
    sys.exit(main())
