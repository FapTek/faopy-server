import asyncio
import websockets
from multiprocessing import Process, Manager
from core.world import World
tickTime = 1 / 32


class Player:
    def __init__(self, Q):
        # TODO Bind game object object
        self.game_object = None
        self.Q = Q  # Players multiprocessing input Queue
        #  Data for sending to client
        self.state = ""  # Information about players health, bullets etc.
        self.view = ""  # Players view zone


def dictCheck(func):  # Decorator checking if token is in dict.
    def validCheck(*args, **kvargs):
        if args[1] in bigDict.dictionary.keys():
            return func(*args, **kvargs)
        else:
            print("KEY ERROR {} : {}".format(func.__name__, args[1]))
            return 0
    return validCheck


class BigDict:  # multiprocessing dictionary for player objects
    def __init__(self):
        self.dictionary = Manager().dict()

    def appendPlayer(self, token, player):
        self.dictionary[token] = {"flag": None, "player": player}

    @dictCheck
    def setFlag(self, token, F):
        # The only way to update multiprocessing objects
        dump = self.dictionary[token]
        dump["flag"] = F
        self.dictionary[token] = dump

    @dictCheck
    def incrFlag(self, token):
        dump = self.dictionary[token]
        dump["flag"] += 1
        self.dictionary[token] = dump

    @dictCheck
    def decrFlag(self, token):
        dump = self.dictionary[token]
        dump["flag"] -= 1
        self.dictionary[token] = dump

    @dictCheck
    def setPlayer(self, token, player):
        # The only way to update multiprocessing objects
        dump = self.dictionary[token]
        dump["flag"] += 1
        dump["player"] = player
        self.dictionary[token] = dump

    @dictCheck
    def getFlag(self, token):
        return self.dictionary[token]["flag"]

    @dictCheck
    def getPlayer(self, token):
        return self.dictionary[token]["player"]


def server(bigDict):
    M = Manager()  # Multiprocessing manager for creating queues

    async def handler(websocket, path):
        Q = M.Queue()  # Player's input queue
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
            bigDict.decrFlag(token)
            player = bigDict.getPlayer(token)
            C = str(player.state)
            V = str(player.view)
            tmp = "state: {}, view: {}".format(C, V)

            # Information handling here

            await websocket.send(str(tmp))

    # start_server = websockets.serve(handler, '10.147.17.206', 9190)
    start_server = websockets.serve(handler, 'localhost', 9000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    bigDict = BigDict()  # multiprocessing dict for players
    server = Process(name="server", target=server,
                     args=(
                         bigDict, ))

    world = World(bigDict)
    tick = Process(name="tick", target=world.start_main_loop)

    server.start()
    tick.start()
    tick.join()
    server.join()
