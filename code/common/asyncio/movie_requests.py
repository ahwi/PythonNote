import requests
from lxml import etree
from time import time

url = 'https://movie.douban.com/top250'


def fetch_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
    response = requests.get(url, headers=headers)
    return response


def parse(url):
    response = fetch_page(url)
    page = response.content
    html = etree.HTML(page)

    xpath_movie = '//*[@id="content"]/div/div[1]/ol/li'
    xpath_title = './/span[@class="title"]'
    xpath_pages = '//*[@id="content"]/div/div[1]/div[2]/a'

    pages = html.xpath(xpath_pages)
    fetch_list = []
    result = []

    for element_movie in html.xpath(xpath_movie):
        result.append(element_movie)

    for p in pages:
        fetch_list.append(url + p.get('href'))

    for url in fetch_list:
        response = fetch_page(url)
        page = response.content
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)

    for i, movie in enumerate(result, 1):
        title = movie.find(xpath_title).text
        print(i, title)


def main():
    from time import time
    start = time()
    for i in range(5):
        parse(url)
    end = time()
    print('Cost {} seconds'.format((end - start) / 5))


if __name__ == '__main__':
    main()

