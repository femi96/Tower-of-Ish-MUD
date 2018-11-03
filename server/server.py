import select
import sys
import asyncio
import websockets

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print("Correct usage: script.py, IP address, port number")
    exit()

print("Start-up successful")

# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
Port = int(sys.argv[2])


class Server():

    def __init__(self):
        """
        Constructor for server

        Asynch threadsafety via monitor pattern

        Server contains a list of clients connected to the server
        """
        self.lock = asyncio.Lock()
        self.list_of_clients = []

    async def add_client(self, client):
        """
        Add the client connection object to the Server
        """
        async with self.lock:
            addr = "<" + str(client.remote_address) + "> "
            print("Added: ", addr)
            self.list_of_clients.append(client)

    async def remove(self, client):
        """
        Removes the connection object from the Server
        """
        async with self.lock:
            if client in self.list_of_clients:
                addr = "<" + str(client.remote_address) + "> "
                print("Removed: ", addr)
                self.list_of_clients.remove(client)

    async def broadcast(self, message, src):
        """
        Broadcast message to all clients not the same as the src
        """
        async with self.lock:
            print(message)
            for client in self.list_of_clients:
                if client != src:
                    await client.send(message)

server = Server()

async def client_coroutine(connection, path):

    # Setup server for client coroutine
    await server.add_client(connection)
    addr = "<" + str(connection.remote_address) + "> "

    while True:
        try:

            message = await connection.recv()
            if message:
                # Calls broadcast function to send message to all
                # broadcast(message_to_send, conn)
                message_to_send = addr + str(message)
                await server.broadcast(message_to_send, connection)

        except Exception as e:
            # Raised exception or connection closed:
            #   remove connection from list and end async thread
            print(e)
            await server.remove(connection)
            return

# Start websockets server with client coroutine
start_server = websockets.serve(client_coroutine, IP_address, Port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
