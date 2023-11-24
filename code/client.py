import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

done = False
while not done:
    input_var = input("Mensagem: ")
    response = input_var.encode('utf-8')
    if input_var == "QUIT":
        done = True

    client.send(response)

    if done: break

    msg = client.recv(1024).decode('utf-8')
    print(msg)

client.close()
