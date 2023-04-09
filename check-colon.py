import json
import os
from os import path


def main():
    year_items = os.listdir(".")
    for year_item in year_items:
        if not path.isdir(year_item):
            continue
        bundle_items = os.listdir(year_item)
        for bundle_item in bundle_items:
            bundle_dir = path.join(year_item, bundle_item)
            if not path.isdir(bundle_dir):
                continue
            json_file = path.join(bundle_dir + ".json")

            tape = False

            if path.exists(json_file):
                with open(json_file, "r") as f:
                    meta = json.load(f)
                tape = 'tape' in meta and meta['tape']

            if not tape:
                break

            for root, dirs, files in os.walk(bundle_dir):
                for f in files:
                    full_path = path.join(root, f)
                    if ":" in full_path:
                        print("Found colon in file name:", full_path)


if __name__ == '__main__':
    main()
