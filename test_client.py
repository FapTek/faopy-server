import asyncio
import websockets
import uuid


async def hello():
    async with websockets.connect('ws://localhost:9000') as websocket:
        hi = str(uuid.uuid4())  # TODO remeber token
        print(hi)
        await websocket.send(hi)
        HI = await websocket.recv()
        print(HI)
        await producer(websocket)



async def consumer(websocket):
    pass

async def producer(websocket):
    while True:
        actions = input("What's happend?: ")
        await websocket.send(actions)


asyncio.get_event_loop().run_until_complete(hello())
