import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def main():
    print("main开始")

    task_list = [
        # python3.8的asyncio.create_task 有个name参数，可以给task取名字
        asyncio.create_task(func()),
        asyncio.create_task(func())
    ]

    print("main结束")

    done, pending = await asyncio.wait(task_list, timeout=None)
    print(done)

asyncio.run(main())

