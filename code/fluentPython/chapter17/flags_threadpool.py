from concurrent import futures

from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor: # executor.__exit__方法会调用executor.shutdown(wait=True)方法，它会在所有线程都执行完毕前阻塞线程
        res = executor.map(download_one, sorted(cc_list)) # map方法返回一个生成器，因此可以迭代，获取各个函数返回的值
    return len(list(res)) # 获取返回的结果数量。如果由线程抛出异常，异常会在这里抛出，这与隐式调用next()函数从迭代器获取相应的返回值一样


if __name__ == "__main__":
    main(download_many)