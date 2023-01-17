from urllib.request import urlopen
import warnings
import os
import json


URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'


def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)


def main():
    feed = load()
    print(sorted(feed['Schedule'].keys()))
    print('*' * 10)
    for key, value in sorted(feed['Schedule'].items()):
        print('{:3}{}'.format(len(value), key))

    print('*' * 10)
    print(feed['Schedule']['speakers'][-1]['name'])
    print(feed['Schedule']['speakers'][-1]['serial'])
    print(feed['Schedule']['events'][40]['name'])
    print(feed['Schedule']['events'][40]['speakers'])

if __name__ == '__main__':
    main()
