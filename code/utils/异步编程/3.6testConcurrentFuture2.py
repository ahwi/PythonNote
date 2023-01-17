import time
import asyncio
import concurrent.futures


def func1():
    # 某个耗时操作
    time.sleep(2)
    return "结果"


async def main():
    loop = asyncio.get_running_loop()
    # 1. Run in the default loop's executor(默认ThreadPoolExecutor)
    # 第一步：内部会线调用ThreadPoolExecutor的submit方法取线程池中申请一个线程去执行func1函数，
    #        并返回一个concurrent.futures.Future对象
    # 第二步：调用asyncio.wrap_future将concurrent.futures.Future对象包装为asyncio.Future对象，
    #        因为concurrent.future.Future对象不支持await语法，所以需要包装为asyncio.Future对象才能使用
    fut = loop.run_in_executor(None, func1)
    result = await fut
    print("default thread pool", result)

    # # 2. Run in a custom thread pool
    # with concurrent.futures.ThreadPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool, func1)
    #     print("custom thread pool", result)
    #
    # # 3. Run in a custom process pool:
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(pool, func1)
    #     print("custom process pool", result)


asyncio.run(main())
