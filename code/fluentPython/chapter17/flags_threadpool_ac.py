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
    with futures.ThreadPoolExecutor(workers) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc) # executor.submit()方法排定可调用对象的执行时间，然后返回一个future，表示这个待执行的操作
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))
        
        results = []
        for future in future.as_complete(to_do): # as_completed函数在future运行结束后产出future
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)
    return len(results)


if __name__ == "__main__":
    main(download_many)