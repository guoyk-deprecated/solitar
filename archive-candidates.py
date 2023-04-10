import json
import subprocess
from typing import List


def main():
    with open('candidates.json', 'r') as f:
        data = json.load(f)

    root: str = data['root']
    items: List[str] = data['items']

    subprocess.run(['tar', '-C', root, '-b', '2048', '-cvf', '/dev/st0', *items], check=True)


if __name__ == '__main__':
    main()
