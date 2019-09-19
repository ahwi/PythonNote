from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import requests
import os
import time

def get(url):
    print('%s GET %s' %(os.getpid(),url))
    response=requests.get(url)
    if response.status_code == 200:
        return {'url':url,'text':response.text}

def parse(res):
    res=res.result()
    url=res['url']
    text=res['text']
    print('%s parse %s res:%s' %(os.getpid(),url,len(text)))


if __name__ == '__main__':
    urls = [
        'https://www.baidu.com',
        'https://www.python.org',
        'https://www.openstack.org',
        'https://help.github.com/',
        'http://www.sina.com.cn/'
    ]

    p = ProcessPoolExecutor()
    start = time.time()
    for url in urls:
        future = p.submit(get, url)
        future.add_done_callback(parse)  # parse(futrue)
    p.shutdown(wait=True)
    print(time.time()-start)  # 3.1761815547943115
    print(os.getpid())
