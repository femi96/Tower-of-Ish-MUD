# Python program to implement server side of chat room.
import select
import sys
from _thread import *
import asyncio
import websockets

"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

print("Start-up successful")

# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
Port = int(sys.argv[2])

# List of clients connected to the server
list_of_clients = []

# CHECK PYTHON THREADSAFETY AND ASYNC ===============================


def remove(connection):
    """
    The following function simply removes the object
    from the list that was created at the beginning of
    the program
    """
    if connection in list_of_clients:
        addr = "<" + str(connection.remote_address) + "> "
        print("Remove: ", addr)
        list_of_clients.remove(connection)

async def client_coroutine(connection, path):

    # Setup server for client coroutine
    list_of_clients.append(connection)
    addr = "<" + str(connection.remote_address) + "> "

    while True:
        try:

            message = await connection.recv()
            if message:

                message_to_send = addr + str(message)
                print(message_to_send)

                # Calls broadcast function to send message to all
                # broadcast(message_to_send, conn)
                response = message_to_send
                await connection.send(response)

        except:
            # Raised connection closed:
            #   remove connection from list and end thread
            remove(connection)
            return

start_server = websockets.serve(client_coroutine, IP_address, Port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
# server.bind((IP_address, Port))

""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
# server.listen(100)


# def clientthread(conn, addr):

#     # sends a message to the client whose user object is conn
#     conn.send("Welcome to this chatroom!".encode('utf-8'))

#     while True:
#         try:
#             message = conn.recv(2048)
#             if message:
#                 print()
#                 print('Message: ', message)

#                 """prints the message and address of the
#                 user who just sent the message on the server
#                 terminal"""
#                 print()
#                 print("here")
#                 print("<" + addr[0] + "> ", message)

#                 # Calls broadcast function to send message to all
#                 message_to_send = "<" + addr[0] + "> " + str(message)
#                 broadcast(message_to_send, conn)
#                 print("end")

#             else:
#                 """message may have no content if the connection
#                 is broken, in this case we remove the connection"""
#                 # remove(conn)
#                 return

#         except:
#             continue


# def broadcast(message, connection):
#     """Using the below function, we broadcast the message to all
#     clients who's object is not the same as the one sending
#     the message """
#     for clients in list_of_clients:
#         if clients != connection:
#             try:
#                 clients.send(message)
#             except:
#                 clients.close()

#                 # if the link is broken, we remove the client
#                 remove(clients)


# while True:

#     """Accepts a connection request and stores two parameters,
#     conn which is a socket object for that user, and addr
#     which contains the IP address of the client that just
#     connected"""
#     conn, addr = server.accept()

#     """Maintains a list of clients for ease of broadcasting
#     a message to all available people in the chatroom"""
#     list_of_clients.append(conn)

#     # prints the address of the user that just connected
#     print()
#     print(addr[0] + " connected")
#     print("Address: ", addr)
#     print("Connection: ", conn)

#     # creates and individual thread for every user
#     # that connects
#     start_new_thread(clientthread, (conn, addr))

# conn.close()
# server.close()
