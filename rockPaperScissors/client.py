import pygame
import threading
import socket
from network import Network
import pickle
from classes.button import Button as MyButton
from classes.inputbox import InputBox
from classes.text import Text
from chat.client import client_chat

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Pedra Papel Tesoura: Online")

button_images = [pygame.image.load("../art/icons/pedra.png"),
                 pygame.image.load("../art/icons/papel.png"),
                 pygame.image.load("../art/icons/tesoura.png")]
background_image = pygame.image.load("../art/icons/moldura.png")
conectar_button_image = pygame.image.load("../art/buttons/connect_text.png")

global thread_client_chat

thread_client_chat = threading.Thread()

global ip
global porta
global my_username
global vitorias
global derrotas
vitorias = derrotas = 0

def verificar_conexao(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, porta))
        print(f"Conexão bem-sucedida com {ip}:{porta}")
        return True
    except socket.error as e:
        print(f"Erro ao conectar com {ip}:{porta}: {e}")
        return False
    finally:
        sock.close()


def redrawWindow(win, game, p):
    win.fill((200,200,200))

    if not(game.connected()):
        font = pygame.font.SysFont("roboto", 60)
        text = font.render("Esperando por outro Jogador...", 1, (255,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("roboto", 45)
        text = font.render("Sua Escolha", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Oponente", 1, (255, 0, 0))
        win.blit(text, (430, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Escolhido", 1, (0, 0, 0))
            else:
                text1 = font.render("Esperando...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Escolhido", 1, (0, 0, 0))
            else:
                text2 = font.render("Esperando...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)
        for text in texts_score:
            text.draw(win)

    pygame.display.update()


btns = [MyButton(button_images[0], (103, 500), "Rock", background_image),
        MyButton(button_images[1], (302, 500), "Paper", background_image),
        MyButton(button_images[2], (501, 500), "Scissors", background_image)]
texts_score = [Text(125, 80, "0", (20, 235, 235), 80),
               Text(475, 80, "0", (235, 20, 20), 80)]

def main():
    global ip
    global porta
    global vitorias
    global derrotas

    vitorias = 0
    derrotas = 0
    Text.setText(texts_score[0], str(vitorias))
    Text.setText(texts_score[1], str(derrotas))

    run = True
    clock = pygame.time.Clock()
    n = Network(server=ip, port=porta)
    player = int(n.getP())
    #print("Você é o jogador", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print(">>>>>Não foi possível achar uma partida")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print(">>>>>Nenhum jogador encontrado.")
                break

            font = pygame.font.SysFont("roboto", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Vitória!", 1, (255,0,0))
                vitorias += 1
                texts_score[0].text = str(vitorias)
            elif game.winner() == -1:
                text = font.render("Empate", 1, (255,0,0))
                derrotas += 0.5
                vitorias += 0.5
                texts_score[0].text = str(vitorias)
                texts_score[1].text = str(derrotas)
            else:
                text = font.render("Derrota...", 1, (255, 0, 0))
                derrotas += 1
                texts_score[1].text = str(derrotas)

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.callback)
                        else:
                            if not game.p2Went:
                                n.send(btn.callback)

        redrawWindow(win, game, player)

def menu_screen():
    global ip
    global porta
    global my_username
    global thread_client_chat
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("roboto", 60)
        text = font.render("Clique para Procurar Partida", 1, (255,0,0))
        win.blit(text, (width // 2 - text.get_width() // 2,height // 2 - text.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    if thread_client_chat and not thread_client_chat.is_alive():
        thread_client_chat = threading.Thread(target=client_chat, args=[ip, my_username])
        thread_client_chat.start()

    main()

def hub_screen():
    global thread_client_chat
    global ip
    global porta
    global my_username

    clock = pygame.time.Clock()
    input_box1 = InputBox(300, 300, 140, 32)
    input_box2 = InputBox(300, 400, 140, 32)
    input_box3 = InputBox(300, 500, 140, 32)
    title = Text(75, 80, "Pedra Papel Tesoura", (235, 235, 235), 80)
    title2 = Text(225, 130, "ONLINE", (235, 30, 30), 100)
    text1 = Text(150, 303, "Username:", (220, 220, 220))
    text2 = Text(150, 403, "IP:", (220, 220, 220))
    text3 = Text(150, 503, "Porta:", (220, 220, 220))
    input_boxes = [input_box1, input_box2, input_box3]
    texts = [title, title2, text1, text2, text3]
    buttons = [MyButton(conectar_button_image, (150, 580), "Connect")]
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.click(pos):
                        if btn.callback == "Connect":
                            my_username = InputBox.getText(input_box1)
                            ip = InputBox.getText(input_box2)
                            porta = int(InputBox.getText(input_box3))
                            if verificar_conexao(ip, porta): return

        for box in input_boxes:
            box.update()

        win.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(win)
        for text in texts:
            text.draw(win)
        for btn in buttons:
            btn.draw(win)

        pygame.display.flip()
        clock.tick(60)

print(">>>CONECTE-SE À UMA PARTIDA PARA INCIAR O CHAT<<<")

while True:
    hub_screen()
    menu_screen()
