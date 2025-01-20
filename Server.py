# Импортируем необходимые библиотеки

import socket

import threading

# Создаем класс для сервера

class ChatServer:

    def __init__(self, host='127.0.0.1', port=5555):

        self.host = host

        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind((self.host, self.port))

        self.server.listen()

        self.clients = []

        self.nicknames = []

    # Функция для рассылки сообщений всем клиентам

    def broadcast(self, message):

        for client in self.clients:

            client.send(message)

    # Функция для обработки сообщений от клиента

    def handle(self, client):

        while True:

            try:

                message = client.recv(1024)

                self.broadcast(message)

            except:

                index = self.clients.index(client)

                self.clients.remove(client)

                client.close()

                nickname = self.nicknames[index]

                self.broadcast(f'{nickname} покинул чат!'.encode('utf-8'))

                self.nicknames.remove(nickname)

                break

    # Функция для принятия новых подключений

    def receive(self):

        while True:

            client, address = self.server.accept()

            print(f"Подключен {str(address)}")

            client.send('NICK'.encode('utf-8'))

            nickname = client.recv(1024).decode('utf-8')

            self.nicknames.append(nickname)

            self.clients.append(client)

            print(f"Никнейм клиента: {nickname}")

            self.broadcast(f"{nickname} присоединился к чату!".encode('utf-8'))

            client.send('Подключен к серверу!'.encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client,))

            thread.start()

# Запуск сервера

if __name__ == "__main__":

    server = ChatServer()

    server.receive()

# Этот код создает простой чат-сервер, который принимает подключения от клиентов, рассылает сообщения всем участникам и обрабатывает отключения.
