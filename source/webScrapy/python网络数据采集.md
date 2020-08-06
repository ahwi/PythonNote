# python网络数据采集



## 第一部分 创建爬虫

### 第1章 初见网络爬虫

#### 1.1 网络连接

使用`urllib`抓取网页

```python
from urllib.request import urlopen


html = urlopen("http://pythonscraping.com/pages/page1.html")
print(html.read())
```

#### 1.2 运行BeautifulSoup

安装BeautifulSoup库

```shell
python3 -m pip install beautifulsoup4
```

使用:

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen("http://pythonscraping.com/pages/page1.html")
bsObj = BeautifulSoup(html.read(), "html.parser")
title = bsObj.html.body.h1
print(title)
```

添加异常处理:

```python
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
```



















































