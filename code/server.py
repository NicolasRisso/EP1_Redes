import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, address = server.accept()

done = False

while not done:
    msg = client.recv(1024).decode('utf-8')
    print(msg)

    if msg == "QUIT": 
        done = True
        break

    input_var = input("Mensagem: ")
    response = input_var.encode('utf-8')
    client.send(response)

client.close()