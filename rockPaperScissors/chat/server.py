import socket
import select
from chat.colors import Colors, print_colored

HEADER_LENGTH = 10

IP = "localhost"
PORT = 6968

#Realizamos uma conexão TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Definimos o Socket como reutilizavel -> Ou seja, mesmo que estaja esperando
#uma resposta, ele ainda poderá enviar novas mensagens.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Conecta
server_socket.bind((IP, PORT))

#Define que o Socket ira "ouvir" a novas conexões
server_socket.listen()

#Lista de Sockets e de Clientes
sockets_list = [server_socket]
clients = {}

print_colored("[CHAT]> ", Colors.MAGENTA)
print(f'Servidor ouvindo conexão em {IP}:{PORT}...')


def receive_message(client_socket):
    try:
        #Header contem o tamanho da mensagem que será recebida.
        message_header = client_socket.recv(HEADER_LENGTH)

        #Se não recebermos nada -> O cliente fechou conexão ou caiu.
        if not len(message_header):
            return False

        #Conversão do Header para um valor int.
        message_length = int(message_header.decode('utf-8').strip())

        #Retorna o header com a mensagem do cliente.
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        #Pega o caso em que o cliente fecha brutalmente seu programa (alt + f4) ou (ctrl + C).
        return False

def server_chat():
    while True:

        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        #Ler todas as potenciais novas conexões
        for notified_socket in read_sockets:

            # Se a conexão notificado for um "servidor", nova conexão, aceitaremos-a.
            if notified_socket == server_socket:
                #Aceitamos a conexão
                client_socket, client_address = server_socket.accept()

                #Recebe o nome do cliente
                user = receive_message(client_socket)

                #Se não mandar, o cliente fechou a conexão antes mesmo de começá-la.
                if user is False:
                    continue

                #Adiciona o Socket à lista de sockets de clientes.
                sockets_list.append(client_socket)

                #E salva o username do cliente para uso futuro.
                clients[client_socket] = user

                print_colored("[CHAT]> ", Colors.MAGENTA)
                print('Nova conexão aceita de {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

            # Se a conexão já existir, ela já é um cliente.
            else:

                #Receba a mensagem.
                message = receive_message(notified_socket)

                #Se a mensagem for False, o cliente se desconectou.
                if message is False:
                    print_colored("[CHAT]> ", Colors.MAGENTA)
                    print('Conexão fechada de: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                    #Removemos o cliente da lista de sockets.
                    sockets_list.remove(notified_socket)

                    #E da lista de usuários.
                    del clients[notified_socket]

                    continue

                #Separamos o usuário por Socket notificado, para, assim, sabermos quem ele é
                user = clients[notified_socket]

                print_colored("[CHAT]> ", Colors.MAGENTA)
                print(f'Mensagem recebida de ({user["data"].decode("utf-8")}): {message["data"].decode("utf-8")}')

                #Passamos por todos os clientes.
                for client_socket in clients:

                    #Não mandamos a mensagem do remetente devolta para ele.
                    if client_socket != notified_socket:

                        #Envia a mensagem (com username junto)
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        #Para lidar com algumas exceptions
        for notified_socket in exception_sockets:

            #Remove da Socket List
            sockets_list.remove(notified_socket)

            #Remove da Client list
            del clients[notified_socket]

if __name__ == "__main__":
    server_chat()