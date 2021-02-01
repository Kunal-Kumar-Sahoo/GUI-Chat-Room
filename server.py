import socket
import threading
import argparse

parser = argparse.ArgumentParser(description='Chatroom server')
parser.add_argument('host', help='Interface the server listens at')
parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                    help='TCP port (default 1060)')
args = parser.parse_args()

HOST = args.host
PORT = args.p

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients, nicknames = [], []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} connected joined the chat\n'.encode('utf-8'))
        client.send('Conected to the server'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Server running...')
receive()
