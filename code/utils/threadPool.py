# -*- coding: UTF-8 -*-
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


# 模拟获取网页
def get_html(times):
    time.sleep(times)
    print(f'get page {times}s finish.')
    return times


def test_thread_pool():
    executor = ThreadPoolExecutor(max_workers=2)
    urls = [3, 2, 4, 6, 7, 8]  # 模拟数据
    i = 0
    all_task = [executor.submit(get_html, (url)) for url in urls]

    for future in as_completed(all_task):
        data = future.result()
        print("in main: get page {}s success".format(data))


if __name__ == '__main__':
    test_thread_pool()