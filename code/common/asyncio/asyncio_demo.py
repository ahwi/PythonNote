import asyncio
import time

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(5)
    print("aaaa")
    return x + y

async def print_sum1(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))
    result = await compute(3, 4)

async def print_sum(x, y):
    tasks = [compute(x1, y1) for x1, y1 in [(1, 2), (3, 4)]]
    result = await asyncio.gather(*tasks)
    print(result)
    # print("%s + %s = %s" % (x, y, result))
    # result = await compute(3, 4)

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()