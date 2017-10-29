import asyncio
import websockets
import multiprocessing


connections = {}


class Player:
    def __init__(self, token, websocket):
        self.token = token
        self.websocket = websocket


async def handler(websocket, path):
    token = await websocket.recv()  # Handshake
    if token in connections:  # linking reconnected player with his old object
        connections[token].websocket = websocket
        print("player {} reconnected".format(token))
    else:  # saving new connection
        connections[token] = Player(token, websocket)
        print("player {} connected".format(token))
    await websocket.send("HI")

    while True:

        try:  # connection check
            await asyncio.wait_for(websocket.ping(), timeout=2)
        except:
            print("Player {} disconnected".format(token))
            break

        a = asyncio.ensure_future(consumer(websocket)) # starting to coroutines
        b = asyncio.ensure_future(producer(websocket))
        done, pending = await asyncio.wait(
            [a, b],
            return_when=asyncio.FIRST_COMPLETED, # restarting both, if one returns
        )
        for task in pending:
            task.cancel()


async def consumer(websocket):
    await asyncio.sleep(0)
    try:
        message = await websocket.recv()
        print("Got message: {}".format(message))
    except:
        print("TIME OUT")


async def producer(websocket):
    await asyncio.sleep(10)
    # print("Producer")

start_server = websockets.serve(handler, '10.147.17.206', 9000)
# start_server = websockets.serve(handler, 'localhost', 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
