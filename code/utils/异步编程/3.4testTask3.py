import asyncio


async def func():
    print("start")
    await asyncio.sleep(2)
    print("end")
    return "返回值"


task_list = [
    func(),
    func()
]

done, pending = asyncio.run(asyncio.wait(task_list))
print(done)

