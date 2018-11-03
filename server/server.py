import select
import sys
import asyncio
import websockets

import game.game as g

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print("Correct usage: script.py, IP address, port number")
    exit()

print("Start-up successful")

# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
Port = int(sys.argv[2])


class GameServer():

    def __init__(self):
        """
        Constructor for game server

        Asynch threadsafety via monitor pattern

        GameServer contains client connections and game instance
            clients are in dictionary, mapping username to websocket connection
        """
        self.lock = asyncio.Lock()
        self.client_connections = dict()
        self.game = g.Game()

    async def add_client(self, clientName, clientConnection):
        """
        Add the client connection object to the GameServer
        """
        async with self.lock:
            if clientName not in self.client_connections:
                print("Added: ", clientName)
                self.client_connections[clientName] = clientConnection
                return True
            else:
                print("Add rejected: ", clientName)
                return False

    async def remove(self, clientName):
        """
        Removes the connection object from the GameServer
        """
        async with self.lock:
            if clientName in self.client_connections:
                print("Removed: ", clientName)
                del self.client_connections[clientName]

    async def broadcast(self, message, clientName):
        """
        Broadcast message to all clients not the same as the src
        """
        async with self.lock:
            print(message)
            for client in self.client_connections:
                if client != clientName:
                    await self.client_connections[client].send(message)

server = GameServer()

async def client_coroutine(client, path):
    """
    Takes client websocket connection and processes inputs
    """

    # Setup GameServer for client coroutine

    added_to_server = False
    username = None

    while not added_to_server:
        await client.send("What is your desired username?")

        try:
            message = await client.recv()
            if message:
                # Try to add connection as username to client
                username = str(message)
                added_to_server = await server.add_client(username, client)
                if added_to_server:
                    await client.send("Username accepted!")
                else:
                    await client.send("Username is taken...")

        except Exception as e:
            # Raised exception or connection closed:
            #   remove connection from list and end async thread
            print(e)
            return

    # Receive messages and send to GameServer
    while True:
        try:
            message = await client.recv()
            if message:
                # Calls broadcast function to send message to all
                #   broadcast(message_to_send, conn)
                message_to_send = username + ": " + str(message)
                await server.broadcast(message_to_send, username)

        except Exception as e:
            # Raised exception or connection closed:
            #   remove connection from list and end async thread
            print(e)
            await server.remove(username)
            return

# Start websockets server with client coroutine
start_server = websockets.serve(client_coroutine, IP_address, Port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
