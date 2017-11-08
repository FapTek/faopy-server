import asyncio
import time
import websockets
import multiprocessing
from multiprocessing import Process, Queue, Manager



class Player:
    def __init__(self, token, Q):
        # TODO Bind game object with connection object
        self.game_object = None
        self.Q = Q  # Players multiprocessing input Queue


def server(connections, output_q, Q):

    async def handler(websocket, path):

        # Handshake
        token = await websocket.recv()  # Receiving players token

        if token in connections.keys():  # Reconnect alertion
            print("player {} reconnected".format(token))
        else:  # Saving new connection
            connections[token] = Player(token, Q)
            print("player {} connected".format(token))

        await websocket.send("HI")  # Handshake end

        # Main loop
        while True:
            try:  # Connection check
                await asyncio.wait_for(websocket.ping(), timeout=10)
                # breaking connection if timeout or disconnection
            except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                print("Player {} disconnected".format(token))
                break

            # starting two coroutines
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
            # appending to the clients' inputs Q
            connections[token].Q.put([token, message])
        except (websockets.exceptions.ConnectionClosed):
            print("CONNECTION CLOSED")

    async def producer(websocket):
        await asyncio.sleep(3)
        if not output_q.empty():
            tmp = output_q.get()
            print(tmp)
            # Information handling here
            await websocket.send(str(tmp))

    # start_server = websockets.serve(handler, '10.147.17.206', 9190)
    start_server = websockets.serve(handler, 'localhost', 9000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def tick(connections, output_q):
    while True:
        for i in connections.keys():
            if not connections[i].Q.empty():
                output_q.put(
                    ["SOME RESPONSE FOR: {}".format(" ".join(connections[i].Q.get()))])


if __name__ == '__main__':
    connections = Manager().dict()  # A dict for saving connections
    output_q = Manager().Queue()  # multiprocessing Q for ticks' results
    server = Process(name="server", target=server,
                     args=(connections,
                           output_q, Manager().Queue()))
    tick = Process(name="tick", target=tick, args=(connections, output_q, ))

    server.start()
    tick.start()
    tick.join()
    server.join()
