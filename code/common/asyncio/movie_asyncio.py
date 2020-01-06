#-*- coding:utf-8 -*-
from lxml import etree
from time import time
import asyncio
import aiohttp

url = 'https://movie.douban.com/top250'

async def fetch_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
        "Cookie": r'gr_user_id=f19283d3-788d-4975-9ad8-71a6a393333a; _vwo_uuid_v2=DDE299E252E137AEA6C6A76E363BE0329|178ff0227ca9910ab968513e785f0c50; __gads=ID=f90048725156b32b:T=1543972280:S=ALNI_MZZ0FdH7henPUNo0Q7a63RIiz7PSQ; douban-fav-remind=1; __utmz=223695111.1571581270.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; trc_cookie_storage=taboola%2520global%253Auser-id%3D0dd063f9-4977-4ef7-9cac-e36b9c5afad4-tuct480edc5; bid=PCw7COZtSqE; viewed="5276434"; __utmz=30149280.1574603599.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; __utmc=223695111; __utma=30149280.397238168.1574427407.1576404482.1576424456.4; __utmb=30149280.0.10.1576424456; __utmb=223695111.0.10.1576424456; __utma=223695111.639836612.1571581270.1576404482.1576424456.4; ll="108090"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1576424481%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DwlqvS51AYAMKjHCbNfHETIiHY14UoZ0I_TwteygQrMaA2QvneRUvZ2l1VF6oMQIrBdOL94vKk4kdH1gLpgtfx_%26wd%3D%26eqid%3Db21a288300369361000000035dac6d4a%22%5D; _pk_ses.100001.4cf6=*; __yadk_uid=2gOzSqPhpj2hTQyOG0ZStgr7orlgXwfZ; dbcl2="53747254:6NG8BCI2D1U"; ck=5Svp; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=5e09c47df67c0039.1571581270.4.1576424818.1576404482.'
    }
    async with aiohttp.ClientSession() as session:
        # async with session.get(url, headers=headers, proxy="http://127.0.0.1:1080") as response:
        async with session.get(url, headers=headers) as response:
            return await response.text()


async def parse(url):
    page = await fetch_content(url)
    # print(page)
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

    tasks = [fetch_content(url) for url in fetch_list]
    pages = await asyncio.gather(*tasks)

    for page in pages:
        html = etree.HTML(page)
        for element_movie in html.xpath(xpath_movie):
            result.append(element_movie)

    for i, movie in enumerate(result, 1):
        title = movie.find(xpath_title).text
        print(i, title)


def main():
    loop = asyncio.get_event_loop()
    start = time()
    for i in range(5):
        loop.run_until_complete(parse(url))
        print("1--------")
    end = time()
    print('Cost {} seconds'.format((end - start) / 5))
    loop.close()


if __name__ == '__main__':
    main()

