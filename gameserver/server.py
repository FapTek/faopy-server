import asyncio
import time
import websockets
from multiprocessing import Process, Queue, Manager


class Player:
    def __init__(self, Q):
        # TODO Bind game object object
        self.game_object = None
        self.Q = Q  # Players multiprocessing input Queue
        #  Data for sending to client
        self.condition = ""  # Information about players health, bullets etc.
        self.view = ""  # Players view zone


class BigDict:  # multiprocessing dictionary for player objects
    def __init__(self):
        self.dictionary = Manager().dict()

    def appendPlayer(self, token, player):
        self.dictionary[token] = {"flag": None, "player": player}

    def setFlag(self, token, F):
        # The only fucking way to update multiprocessing objects
        dump = self.dictionary[token]
        dump["flag"] = F
        self.dictionary[token] = dump

    def setPlayer(self, token, player):
        # The only fucking way to update multiprocessing objects
        dump = self.dictionary[token]
        dump["flag"] = 1
        dump["player"] = player
        self.dictionary[token] = dump

    def getFlag(self, token):
        return self.dictionary[token]["flag"]

    def getPlayer(self, token):
        return self.dictionary[token]["player"]


def server(bigDict, Q):

    async def handler(websocket, path):

        # Handshake
        token = await websocket.recv()  # Receiving players token

        if token in bigDict.dictionary.keys():  # Reconnect alertion
            print("player {} reconnected".format(token))
        else:  # Saving new connection
            player = Player(Q)
            bigDict.appendPlayer(token, player)
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
            b = asyncio.ensure_future(producer(websocket, token))
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
            bigDict.getPlayer(token).Q.put([message])
        except (websockets.exceptions.ConnectionClosed):
            print("CONNECTION CLOSED")

    async def producer(websocket, token):
        if bigDict.getFlag(token):
            bigDict.setFlag(token, 0)
            player = bigDict.getPlayer(token)
            C = str(player.condition)
            V = str(player.view)
            tmp = "condition: {}, view: {}".format(C, V)
            # Information handling here
            await websocket.send(str(tmp))

    # start_server = websockets.serve(handler, '10.147.17.206', 9190)
    start_server = websockets.serve(handler, 'localhost', 9000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def tick(bigDict):
    while True:
        for token in bigDict.dictionary.keys():
            if not bigDict.getPlayer(token).Q.empty():
                data = bigDict.getPlayer(token).Q.get()
                # TODO implement me
                player = bigDict.getPlayer(token)
                player.condition = data
                player.view = data
                bigDict.setPlayer(token, player)


if __name__ == '__main__':
    bigDict = BigDict()  # multiprocessing dict for players
    server = Process(name="server", target=server,
                     args=(
                           bigDict, Manager().Queue()))
    tick = Process(name="tick", target=tick, args=(bigDict, ))

    server.start()
    tick.start()
    tick.join()
    server.join()
