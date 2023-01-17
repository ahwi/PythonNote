import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


async def main():
    print("main开始")

    # 创建Task对象，将当前执行func函数任务添加到事件循环
    task1 = asyncio.create_task(func())

    # 创建Task对象，将当前执行func函数任务添加到事件循环
    task2 = asyncio.create_task(func())

    print("main结束")

    # 当执行某个协程遇到IO操作时，会自动切换执行其他任务
    # 此处的await是等待相应的协程全部执行完毕并获取结果
    ret1 = await task1  # 会等task1返回值才继续往下执行下一条语句
    ret2 = await task2
    print(ret1, ret2)

asyncio.run(main())

