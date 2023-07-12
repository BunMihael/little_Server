import socket
import threading

class Client:
    def __init__(self, host, port, nickname):
        # The client's nickname
        self.nickname = nickname
        # Create a new client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        self.client.connect((host, port))

    def receive(self):
        # Continuously receive messages from the server
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    # If the server is asking for our nickname, send it
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    # Otherwise, print the received message
                    print(message)
            except socket.error:
                # If an error occurs, close the client connection
                print("An error occurred!")
                self.client.close()
                break

    def write(self):
        # Continuously read user input and send messages to the server
        while True:
            message = f'{self.nickname} {input("")}'
            self.client.send(message.encode('ascii'))

if __name__ == "__main__":
    # Ask for the user's nickname
    nickname = input("Enter your nickname: ")
    # Create a new client and start communication
    client = Client('127.0.0.1', 55555, nickname)

    # Start a new thread for receiving messages from the server
    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    # Start a new thread for sending messages to the server
    write_thread = threading.Thread(target=client.write)
    write_thread.start()
