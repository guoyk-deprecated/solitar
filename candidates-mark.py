import json
from os import path
from typing import List


def main():
    with open('candidates.json', 'r') as f:
        data = json.load(f)

    root: str = data['root']
    items: List[str] = data['items']

    for item in items:
        bundle_json = path.join(root, item + ".json")
        if path.exists(bundle_json):
            with open(bundle_json, 'r') as f:
                meta = json.load(f)
            meta['tape'] = True
        else:
            meta = {'tape': True}
        with open(bundle_json, 'w') as f:
            json.dump(meta, f)

        print(f"Marked {item} as taped")


if __name__ == '__main__':
    main()
