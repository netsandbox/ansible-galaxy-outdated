"""ansible-galaxy-outdated."""

import json
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


def _get_latest_version(collection):
    url = f"https://galaxy.ansible.com/api/v2/collections/{collection.replace('.', '/')}/"

    with urllib.request.urlopen(url) as f:
        galaxy_data = json.load(f)

    if galaxy_data["deprecated"]:
        print(f"WARNING: collection {collection} is deprecated")

    return galaxy_data["latest_version"]["version"]


def main():
    """Run main function."""
    try:
        collections_json = subprocess.check_output(["ansible-galaxy", "collection", "list", "--format=json"])
    except FileNotFoundError:
        sys.exit("ansible-galaxy not found")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ansible-galaxy error: {e}")

    collections = json.loads(collections_json)
    collections = collections[list(collections.keys())[0]]

    data = []
    for k, v in sorted(collections.items()):
        data.append(dict(name=k, version=v["version"], latest=_get_latest_version(k)))

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


if __name__ == "__main__":
    main()
