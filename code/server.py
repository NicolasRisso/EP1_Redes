import socket
import struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, address = server.accept()

username = input("Username: ")

done = False
while not done:
    #Recebe o tamanho do username e depois o username
    response_username_length = struct.unpack('!I', client.recv(4))[0]
    response_username = client.recv(response_username_length).decode('utf-8')

    #Recebe o tamanho da mensagem e depois a mensagem
    message_length = struct.unpack('!I', client.recv(4))[0]
    message = client.recv(message_length).decode('utf-8')

    print(f"({response_username}): {message}")

    if message == "QUIT":
        done = True
    else:
        # Respond to the client
        response = input(f"({username}): ")
        
        # Send the length of the response and the response itself
        client.send(struct.pack('!I', len(username)))
        client.send(username.encode('utf-8'))

        client.send(struct.pack('!I', len(response)))
        client.send(response.encode('utf-8'))

client.close()
