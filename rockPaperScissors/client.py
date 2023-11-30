import pygame
import threading
from network import Network
import pickle
from button import Button as MyButton
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


def redrawWindow(win, game, p):
    win.fill((200,200,200))

    if not(game.connected()):
        font = pygame.font.SysFont("roboto", 60)
        text = font.render("Esperando por outro Jogador...", 1, (255,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("roboto", 45)
        text = font.render("Sua Escolha", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Escolha do Oponente", 1, (0, 255, 255))
        win.blit(text, (380, 200))

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

    pygame.display.update()


btns = [MyButton(button_images[0], (103, 500), "Rock", background_image),
        MyButton(button_images[1], (302, 500), "Paper", background_image),
        MyButton(button_images[2], (501, 500), "Scissors", background_image)]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
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
            elif game.winner() == -1:
                text = font.render("Empate", 1, (255,0,0))
            else:
                text = font.render("Derrota...", 1, (255, 0, 0))

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

    thread_client_chat = threading.Thread(target=client_chat)
    thread_client_chat.start()

    main()

print(">>>CONECTE-SE À UMA PARTIDA PARA INCIAR O CHAT<<<")

while True:
    menu_screen()
