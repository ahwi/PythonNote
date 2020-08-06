from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def get_title(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.html.body.h1
    except AttributeError as e:
        return None
    return title


def main():
    title = get_title("http://pythonscraping.com/pages/page1.html")
    if title is None:
        print("Title counld not be found")
    else:
        print(title)


if __name__ == '__main__':
    main()
