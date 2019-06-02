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
import redis
import gevent
from flask import Flask, render_template
from flask_sockets import Sockets

REDIS_URL = os.environ['REDIS_URL']
REDIS_CHAN = 'chat'

app = Flask(__name__)
app.debug = 'DEBUG' in os.environ

sockets = Sockets(app)
redis = redis.from_url(REDIS_URL)

class ChatBackend(object):
    """ Interface que registra e atualiza os clientes do WebSocket"""

    def __init__(self):
        self.clients = list()
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(REDIS_CHAN)

    def register(self, client):
        """Registra a conexão do WebSocket para as atualizações da lista de client."""
        self.clients.append(client)
        print('Num of Clients ', len(self.clients))
        
    def __iter_data(self):
        for message in self.pubsub.listen():
            data = message.get('data')
            if message['type'] == 'message':
                print(u'Sending message: {}'.format(data))
                yield data

    def send(self, client, data):
        """ Envia o dado do cliente registrado e
        automaticamente discarta conexões inválidas"""
        try:
            client.send(data)
            print('Message sent: {}'.format(data))
        except Exception:
            self.clients.remove(client)
            app.logger.exception('error sending message')

    def run(self):
        """Esperando msgs do Redis e enviando aos clientes."""
        for data in self.__iter_data():
            for client in self.clients:
                gevent.spawn(self.send, client, data)

    def start(self):
        """Redis subscription em background."""
        print('Chat started')
        gevent.spawn(self.run)

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
        gevent.sleep(0.1)
        message = ws.receive()
        if message:
            print('Inserting message: {}'.format(message))
            redis.publish(REDIS_CHAN, message)

@sockets.route('/receive')
def outbox(ws):
    """Envia mensagens de bate-papo, via `ChatBackend`."""
    chats.register(ws)

    while not ws.closed:
        # Context switch while `ChatBackend.start` is running in the background.
        gevent.sleep(0.1)



