import json
import os
import re
import sys
from os import path

SIZE_THRESHOLD = 1300 * 1024 * 1024 * 1024  # 1.3 TB for LTO-5

SKIPPING_DIRS = ['@eaDir', 'lost+found']


def main():
    src_dir = sys.argv[1]

    print('Source Dir: ' + src_dir)

    candidates = []
    candidates_size = 0

    exceeded = False
    for year_name in os.listdir(src_dir):
        if exceeded:
            break

        if not re.match(r'\d{4}', year_name):
            continue

        year_dir = path.join(src_dir, year_name)

        if not path.isdir(year_dir):
            continue

        for bundle_name in os.listdir(year_dir):

            if bundle_name in SKIPPING_DIRS:
                continue

            bundle_dir = path.join(year_dir, bundle_name)

            if not path.isdir(bundle_dir):
                continue

            bundle_json = path.join(year_dir, bundle_name + '.json')

            if path.exists(bundle_json):
                with open(bundle_json, 'r') as f:
                    meta = json.load(f)
                if 'tape' in meta and meta['tape']:
                    print('Skipping: ' + bundle_dir + ', because it is already taped')
                    continue

            print('Calculating: ' + bundle_name)

            bundle_size = 0

            for root, dirs, files in os.walk(path.join(year_dir, bundle_name)):
                for f in files:
                    try:
                        bundle_size += path.getsize(path.join(root, f))
                    except FileNotFoundError:
                        print('File not found: ' + path.join(root, f))

            if candidates_size + bundle_size > SIZE_THRESHOLD:
                exceeded = True
                break

            print("Bundle: " + bundle_name + " is " + str(bundle_size) + " bytes")

            candidates.append(bundle_dir)
            candidates_size += bundle_size

            print('Candidates Size: ' + str(candidates_size))

    print(candidates)
    print(candidates_size)

    with open('candidates.json', 'w') as f:
        json.dump({
            'root': src_dir,
            'items': [path.relpath(item, src_dir) for item in candidates],
        }, f, indent=4)


if __name__ == '__main__':
    main()
