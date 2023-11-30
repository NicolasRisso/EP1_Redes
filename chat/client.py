import socket
import select
import errno
import sys
import threading

HEADER_LENGTH = 10

IP = "localhost"
PORT = 6969
my_username = input("Username: ")

#Cria um Socket TCP para se comunicar com o servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conecta
client_socket.connect((IP, PORT))

#Define a conexão para um estado de "não bloqueamento", assim, o código não ficará travado
#enquanto espera uma resposta do servidor.
client_socket.setblocking(False)

#Prepara o header e a mensagem contendo o Username e os envia.
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    #PROBLEMA AQUI, ISSO NÃO DEIXA DINAMICO A RECEPÇÃO
    #Espera até o usuário digitar sua mensagem
    message = input(f'{my_username}: ')

    #Se a mensagem não for vazio, a envia.
    if message:

        #Encoda a mensagem em bytes e a envia junto com o header.
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        #loop entre todas as mensagens recebidas nesse meio tempo.
        while True:

            #Header
            username_header = client_socket.recv(HEADER_LENGTH)

            #Servidor fechou a conexão
            if not len(username_header):
                print('Conexão desligada pelo Servidor')
                sys.exit()

            #Header -> int
            username_length = int(username_header.decode('utf-8').strip())

            #Decodifica o username
            username = client_socket.recv(username_length).decode('utf-8')

            #Decodifica a mensagem (com header)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username}: {message}')

    except IOError as e:
        #Detectar possíveis erros do sistema.
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        #Se chegar aqui, não tem erro.
        continue

    except Exception as e:
        #Qualquer outra exception, como um exit.
        print('Reading error: '.format(str(e)))
        sys.exit()