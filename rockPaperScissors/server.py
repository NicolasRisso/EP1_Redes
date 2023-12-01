import socket
import pickle
import threading
from _thread import *
from game import Game
from chat.server import server_chat
from chat.colors import Colors, print_colored

server = "localhost"
port = 6969

tmp2 = input("Digite o seu ip para hospedar o Servidor: ")
if tmp2 != "": server = tmp2 
tmp = input("Digite a porta do Servidor: ")
if tmp != "" and int(tmp) is int: port = tmp

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print_colored("[GAME]> ", Colors.GREEN)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break
    print_colored("[GAME]> ", Colors.GREEN)
    print("Conexão Perdida")
    try:
        del games[gameId]
        print_colored("[GAME]> ", Colors.GREEN)
        print("Fechando Jogo", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print_colored("[GAME]> ", Colors.GREEN)
    print("Conectado à:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print_colored("[GAME]> ", Colors.GREEN)
        print("Criando novo jogo...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))

    once = True
    if once:
        thread_server_chat = threading.Thread(target=server_chat, args=(server,))
        thread_server_chat.start()
        once = False