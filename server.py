import asyncio
import time
import websockets
import multiprocessing
from multiprocessing import Process, Queue

def server(input_q, output_q):
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
                await asyncio.wait_for(websocket.ping(), timeout=1)
            except:
                print("Player {} disconnected".format(token))
                break

            a = asyncio.ensure_future(consumer(websocket, token)) # starting to coroutines
            b = asyncio.ensure_future(producer(websocket))
            done, pending = await asyncio.wait(
                [a, b],
                return_when=asyncio.FIRST_COMPLETED, # restarting both, if one returns
            )
            for task in pending:
                task.cancel()


    async def consumer(websocket, token):
        await asyncio.sleep(0)
        try:
            message = await websocket.recv()
            print("Got message: {}".format(message))
            input_q.put([token, message])
        except:
            pass
            # print("TIME OUT")


    async def producer(websocket):
        # await asyncio.sleep(0)
        if not output_q.empty():
            print("".join(output_q.get()))

    start_server = websockets.serve(handler, '10.147.17.206', 9190)
    # start_server = websockets.serve(handler, 'localhost', 9000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def tick(input_q, output_q):
    while True:
        if not input_q.empty():
            output_q.put(["SOME RESPONSE FOR: {}".format(" ".join(input_q.get()))])


if __name__ == '__main__':
    input_q = Queue()
    output_q = Queue()
    server = Process(name="server", target=server,  args=(input_q, output_q, ))
    test = Process(name="tick", target=tick, args=(input_q, output_q, ))

    server.start()
    test.start()
    test.join()
