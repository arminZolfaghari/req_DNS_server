# part 2 client
import socket
from threading import Thread


def send_msg():
    message = input()
    client_socket.send(bytes(message, "utf8"))

    if message == "-quit":
        client_socket.close()
        print('CHAT > Disconnected Successfully!')
        global terminate
        terminate = True


def receive_msg():
    while True:
        try:
            incoming_message = client_socket.recv(1024).decode("utf8")
            print('\n>', incoming_message)
        except OSError:
            break


if __name__ == "__main__":
    # creating socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 4444)
    client_socket.connect(server_address)
    message = input('Enter your message: ')
    client_socket.send(bytes(message, 'utf-8'))

    receiver = Thread(target=receive_msg)
    receiver.start()
    terminate = False

    while True:
        send_msg()
        if terminate:
            break
