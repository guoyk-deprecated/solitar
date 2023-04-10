import json
import os
import re
from os import path

SIZE_THRESHOLD = 1300 * 1024 * 1024 * 1024  # 1.3 TB for LTO-5

SKIPPING_DIRS = ['@eaDir', 'lost+found']


def main():
    candidates = []
    candidates_size = 0

    exceeded = False
    for dir_year in os.listdir('.'):
        if exceeded:
            break

        if not path.isdir(dir_year):
            continue

        if not re.match(r'\d{4}', dir_year):
            continue

        for bundle_item in os.listdir(dir_year):

            if bundle_item in SKIPPING_DIRS:
                continue

            bundle_dir = path.join(dir_year, bundle_item)

            if not path.isdir(bundle_dir):
                continue

            bundle_json = path.join(dir_year, bundle_item + '.json')

            if path.exists(bundle_json):
                with open(bundle_json, 'r') as f:
                    meta = json.load(f)
                if 'tape' in meta and meta['tape']:
                    print('Skipping: ' + bundle_dir + ', because it is already taped')
                    continue

            print('Calculating: ' + bundle_item)

            bundle_size = 0

            for root, dirs, files in os.walk(path.join(dir_year, bundle_item), topdown=True):
                for f in files:
                    try:
                        bundle_size += path.getsize(path.join(root, f))
                    except FileNotFoundError:
                        print('File not found: ' + path.join(root, f))

            if candidates_size + bundle_size > SIZE_THRESHOLD:
                exceeded = True
                break

            candidates.append(path.join(dir_year, bundle_item))
            candidates_size += bundle_size

            print('Candidates Size: ' + str(candidates_size))

    print(candidates)
    print(candidates_size)

    with open('candidates.json', 'w') as f:
        json.dump(candidates, f, indent=4)


if __name__ == '__main__':
    main()
