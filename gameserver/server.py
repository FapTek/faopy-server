import asyncio
import time
import websockets
import multiprocessing
from multiprocessing import Process, Queue


class Player:
    def __init__(self, token, websocket):
        self.token = token
        self.websocket = websocket


def server(input_q, output_q):
    connections = {}  # A dict for saving connections

    async def handler(websocket, path):
        # Handshake
        token = await websocket.recv()  # Receiving players token
        # Linking reconnected player with his old object
        if token in connections:
            connections[token].websocket = websocket
            print("player {} reconnected".format(token))
        else:  # Saving new connection
            connections[token] = Player(token, websocket)
            print("player {} connected".format(token))
        await websocket.send("HI")

        # Main loop
        while True:
            try:  # Connection check
                await asyncio.wait_for(websocket.ping(), timeout=10)
                # breaking connection if player disconnected
            except (asyncio.TimeoutError):
                print("Player {} disconnected".format(token))
                break

            # starting to coroutines
            a = asyncio.ensure_future(consumer(websocket, token))
            b = asyncio.ensure_future(producer(websocket))
            done, pending = await asyncio.wait(
                [a, b],
                return_when=asyncio.FIRST_COMPLETED,
            )
            # restarting both, if one returns
            for task in pending:
                task.cancel()

    async def consumer(websocket, token):
        try:
            message = await websocket.recv()
            print("Got message: {}".format(message))
            input_q.put([token, message])  # appending to the clients' inputs Q
        except (websockets.exceptions.ConnectionClosed):
            pass
            print("CONNECTION CLOSED")

    async def producer(websocket):
        if not output_q.empty():
            print("".join(output_q.get()))

    # start_server = websockets.serve(handler, '10.147.17.206', 9190)
    start_server = websockets.serve(handler, 'localhost', 9000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def tick(input_q, output_q):
    while True:
        if not input_q.empty():
            output_q.put(
                ["SOME RESPONSE FOR: {}".format(" ".join(input_q.get()))])


if __name__ == '__main__':
    input_q = Queue()  # multiprocessing Q for clients' inputs
    output_q = Queue()  # multiprocessing Q for ticks' results
    server = Process(name="server", target=server,  args=(input_q, output_q, ))
    tick = Process(name="tick", target=tick, args=(input_q, output_q, ))

    server.start()
    tick.start()
    tick.join()
    server.join()
