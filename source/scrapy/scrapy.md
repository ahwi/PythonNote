# scrapy教程

## 初探

本节目标:

1. Creating a new Scrapy project
2. Writing a [spider](https://docs.scrapy.org/en/latest/topics/spiders.html#topics-spiders) to crawl a site and extract data
3. Exporting the scraped data using the command line
4. Changing spider to recursively follow links
5. Using spider arguments

**创建工程:**

```
scrapy startproject tutorial
```

创建出来的目录:

```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

