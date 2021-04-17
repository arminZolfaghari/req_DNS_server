# part2 server
import socket
from threading import Thread


def client_handler(client, addr, name):

    while True:
        msg = client.recv(size)
        msg = str(msg, 'utf-8')
        msg = msg.rstrip("\n")
        print(msg)


if __name__ == "__main__":
    size = 1024
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 4444))
    server_socket.listen(5)

    print('Waiting for Client to connect...')

    while True:
        client_socket, address = server_socket.accept()
        client_name = client_socket.recv(size).decode()
        print('connected :', client_name, address, '.')
        # addresses[c] = address
        # c.send(bytes('welcome ' + client_name, 'utf-8'))
        Thread(target=client_handler, args=(client_socket, address, client_name)).start()
