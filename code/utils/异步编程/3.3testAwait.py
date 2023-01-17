import asyncio


async def func():
    print("hello")
    response = await asyncio.sleep(2)
    return response

asyncio.run(func())
