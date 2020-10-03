#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import numpy as np


def accept_incoming_connections():
    """Lidar com a conexao de novos clientes (eleitores)"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s está online." % client_address)
        client.send(bytes("Bem vindo a urna!@Coloque seu nome e a legenda do candidato.", "utf8"))
        addresses[client] = client_address #Salvar o endereço do cliente na lista de endereços
        Thread(target=handle_client, args=(client,)).start() #Startar uma nova thread para a atividade de handle_client, passando o cliente como argumento

def handle_client(client): 
    """lidar com a conexao do cliente"""

    msg = client.recv(BUFSIZ).decode("utf8")
    msg_split = msg.split("@")

    name = msg_split[1]
    vote = msg_split[2]

    #Enviar uma mensagem de agradecimento para o cliente
    thankYouMessage = "Voto computado. Obrigado, " + name + "!"
    client.send(bytes(thankYouMessage, "utf8"))

    clients[client] = name
    votes.append(vote)

    #Computar votos
    counts = np.bincount(votes)

    winnerCandidate = np.argmax(counts)
    winnerCandidateVotes = counts[winnerCandidate]

    msg = "O candidato da legenda " + str(winnerCandidate) + " vence por " +  str(winnerCandidateVotes) + " voto(s)."

    broadcast(msg)

def broadcast(msg):
    """Transmitir mensagem com o candidato vencedor para todos os clientes"""

    for sock in clients:
        sock.send(bytes(msg, "utf-8"))


clients = {}
addresses = {}
votes = []

HOST = "localhost"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

#Criar um servidor e configurar a porta
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) 

if __name__ == "__main__":
    #Colocar o servidor para ouvir
    SERVER.listen(5)
    print("Waiting for connection...")

    #Criar uma Thread para rodar a atividade accept_incoming_connections
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)

    #Startar a Thread
    ACCEPT_THREAD.start()

    #Esperar até que a atividade dela termine
    ACCEPT_THREAD.join()

#Fechar a conexao do servidor
SERVER.close()