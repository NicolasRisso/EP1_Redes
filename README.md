# Exercício Programa 1 de Redes de Computadores USP
Esse jogo é o primeiro exercício programa da matéria de Redes de Computadores da USP.

## Conceito
Esse jogo consiste em um Pedra Papel Tesoura ONLINE, em que é possível jogar 1v1 com seus amigos por
meio de uma rede cliente-servidor TCP.
Ele possui entrada para username, ip e porta, assim, tornando possível jogá-lo com amigos em outros
computadores por meio de VPNs como Hamachi.

## Como Rodar
Basta ler o txt "HotToCompile", mas aqui vai um resumo:
1. Instale Python3
2. Instale o Pygame (pip install pygame)
3. Vá até o diretório do jogo (cd rockPapersScissors)
4. Abra o Servidor (python server.js)
5. Em outro terminal, abra os clients (python client.js)
6. No client, por padrão, utilize a porta 6969 para se conectar ao servidor.

## Créditos
Desenvolvido Por:
- Nicolas Pereira Risso Vieira
- Andreas Hukuhara Christe
- Pedro Palazzi de Souza
Os tutoriais abaixo foram de grande ajuda para o desenvolvimento desse projeto:
- https://www.youtube.com/watch?v=ytu2yV3Gn1I
- https://www.techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p-4
