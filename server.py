import socket
import threading

class Server:
    def __init__(self, host, port):
        # Create a new server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to a specific host and port
        self.server.bind((host, port))
        # Listen for incoming connections
        self.server.listen()
        # Use a dictionary to keep track of clients and their nicknames
        self.clients = {}

    def broadcast(self, message):
        # Send a message to all connected clients
        for client in self.clients.keys():
            client.send(message)

    def handle(self, client):
        # Handle communication with a client
        while True:
            try:
                # Receive a message from the client
                message = client.recv(1024)
                # Broadcast the message to all clients
                self.broadcast(message)
            except socket.error:
                # If an error occurs, close the client connection
                client.close()
                # Remove the client from the dictionary
                nickname = self.clients[client]
                self.broadcast(f'{nickname} left!'.encode('ascii'))
                del self.clients[client]
                break

    def receive(self):
        # Continuously accept new connections
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            # Add the client and its nickname to the dictionary
            self.clients[client] = nickname

            print(f"Nickname is {nickname}")
            self.broadcast(f"{nickname} joined!".encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start a new thread to handle this client's communication
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

if __name__ == "__main__":
    print("Server is listening...")
    server = Server('127.0.0.1', 55555)
    server.receive()
