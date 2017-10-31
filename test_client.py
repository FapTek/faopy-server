import asyncio
import websockets
import uuid


async def hello():
    async with websockets.connect('ws://10.147.17.206:9190') as websocket:
        hi = str(uuid.uuid4())  # TODO remeber token
        print(hi)
        await websocket.send(hi)
        HI = await websocket.recv()
        print(HI)
        while True:
            a = asyncio.ensure_future(consumer(websocket))  # starting to coroutines
            b = asyncio.ensure_future(producer(websocket))
            done, pending = await asyncio.wait(
                [a, b],
                return_when=asyncio.FIRST_COMPLETED,  # restarting both, if one returns
            )
            for task in pending:
                task.cancel()


async def consumer(websocket):
    data = await websocket.recv()
    print(f"Response: {data}")


async def producer(websocket):
    actions = input("What's happend?: ")
    await websocket.send(actions)


asyncio.get_event_loop().run_until_complete(hello())
