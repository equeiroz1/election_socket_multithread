#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) election application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import numpy as np


def accept_incoming_connections():
    """Sets up handling for incoming clients (voters)."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s está online." % client_address)
        client.send(bytes("Bem vindo a urna!", "utf8"))
        client.send(bytes("Por favor, coloque seu nome e a legenda do candidato desejado.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


#takes client socket as argument.
def handle_client(client): 
    """Handles client connection"""

    msg = client.recv(BUFSIZ).decode("utf8")
    msg_split = msg.split("@")

    name = msg_split[1]
    vote = msg_split[2]

    #sending thankYou message to the voter
    thankYouMessage = "Voto computado. Obrigado, " + name + "!"
    client.send(bytes(thankYouMessage, "utf8"))

    clients[client] = name
    votes.append(vote)

    #computing votes
    counts = np.bincount(votes)

    winnerCandidate = np.argmax(counts)
    winnerCandidateVotes = counts[winnerCandidate]

    msg = "O candidato da legenda " + str(winnerCandidate) + " vence por " +  str(winnerCandidateVotes) + " voto(s)."

    broadcast(msg)

def broadcast(msg):
    """Broadcasts a message with winner candidate for all clients"""

    for sock in clients:
        sock.send(bytes(msg, "utf-8"))


clients = {}
addresses = {}
votes = []

HOST = "localhost"
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()