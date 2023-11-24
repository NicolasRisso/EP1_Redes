import socket
import struct

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

username = input("Username: ")

done = False
while not done:
    #Pegue a mensagem do usuário
    message = input(f"({username}): ")

    #Mande o tamanho do username e da mensagem, depois envia a mensagem / username em si
    client.send(struct.pack('!I', len(username)))
    client.send(username.encode('utf-8'))

    client.send(struct.pack('!I', len(message)))
    client.send(message.encode('utf-8'))

    if message == "QUIT":
        done = True
    else:
        response_username_lenght =struct.unpack('!I', client.recv(4))[0]
        response_username = client.recv(response_username_lenght).decode('utf-8')
        response_length = struct.unpack('!I', client.recv(4))[0]
        response = client.recv(response_length).decode('utf-8')
        print(f"({response_username}): {response}")

client.close()
