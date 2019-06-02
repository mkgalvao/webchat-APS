# -*- coding: utf-8 -*-

"""
Servidor do chat
===========
Essa aplicação foi desenvolvida como projeto de APS da disciplina de Redes
da Universidade Paulista campus Paraíso. 1/2019 

Gabriel Gomes da Silva – D3967HO
Monica Karoline Silva Galvão – D755226
Nicolay Padalko - D37EII0
Victor Mendes Ribeiro dos Santos – C435244


"""

import os
import logging
import gevent
from flask import Flask, render_template
from flask_sockets import Sockets

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)


class ChatBackend(object):
    """ Interface que registra e atualiza os clientes do WebSocket"""

    def __init__(self):
        self.clients = list()

    def register(self, client):
        """Registra a conexão do WebSocket para as atualizações da lista de client."""
        self.clients.append(client)
        logging.info('client registered')

    def broadcast(self, message):
        if message:
            logging.info('Inserting message: {}'.format(message))
            for client in self.clients:
                gevent.spawn(self.send, client, message)

    def send(self, client, data):
        """ Envia o dado do cliente registrado e
        automaticamente discarta conexões inválidas"""
        try:
            client.send(data)
            logging.info('Message sent: {}'.format(data))
        except Exception:
            self.clients.remove(client)
            logging.exception('error sending message')


    def start(self):
        logging.info('Chat started')

chats = ChatBackend()
chats.start()

@app.route('/')
def hello():
    return render_template('index.html')

@sockets.route('/submit')
def inbox(ws):
    """Recebe as mensaggens do chat e adiciona-as ao broadcast"""
    while not ws.closed:
        # sleep para evitar * constantes * context-switches..
        # gevent.sleep(0.1)
        message = ws.receive()
        chats.broadcast(message)

@sockets.route('/receive')
def outbox(ws):
    """Envia mensagens de bate-papo, via `ChatBackend`."""
    chats.register(ws)

    while not ws.closed:
        # Context switch while `ChatBackend.start` is running in the background.
        gevent.sleep(0.1)