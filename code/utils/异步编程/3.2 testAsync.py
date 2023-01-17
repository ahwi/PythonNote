import asyncio

async def func():
    print("hello")

result = func()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(result)
asyncio.run(result)