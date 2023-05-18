#!/usr/bin/env python3
# encoding: utf-8

import sys
import argparse
import socket
import threading
from PyQt5 import QtWidgets

class ClientGUI(QtWidgets.QWidget):

    def __init__(self, host, port):
        super().__init__()

        self.host = host
        self.port = port

        self.sock = None
        self.messages = []

        self.init_ui()

    def init_ui(self):
        # set up UI elements
        self.message_list = QtWidgets.QListWidget(self)
        self.message_list.setGeometry(10, 10, 280, 200)

        self.message_input = QtWidgets.QLineEdit(self)
        self.message_input.setGeometry(10, 220, 200, 30)
        self.message_input.returnPressed.connect(self.send_message)

        self.send_button = QtWidgets.QPushButton('Send', self)
        self.send_button.setGeometry(220, 220, 70, 30)
        self.send_button.clicked.connect(self.send_message)

        # set up socket connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.messages.append(f"Connected to server at {self.host}:{self.port}")

        # send "connect" request to server
        self.sock.sendall("GET /connect HTTP/1.1\r\nHost: {}\r\n\r\n".format(self.host).encode())

        # receive response from server
        response = self.sock.recv(1024).decode()
        self.messages.append(response)

        # start listening for incoming messages from other clients
        threading.Thread(target=self.listen_for_messages).start()

        # set up UI display
        self.setWindowTitle('Dots and Boxes Chat')
        self.setGeometry(100, 100, 300, 260)
        self.show()

    def send_message(self):
        message = self.message_input.text()
        if message.lower() == "exit":
            self.close()
        encoded_message = message.encode()
        message_length = len(encoded_message)
        request = "POST / HTTP/1.1\r\nHost: {}\r\nContent-Length: {}\r\n\r\n{}".format(self.host, message_length, message)
        self.sock.sendall(request.encode())
        self.message_input.clear()

    def listen_for_messages(self):
        while True:
            message = self.sock.recv(1024).decode()
            if not message:
                break
            self.messages.append(message)
            self.update_message_list()

    def update_message_list(self):
        self.message_list.clear()
        for message in self.messages:
            self.message_list.addItem(message)

    def closeEvent(self, event):
        self.sock.close()
        event.accept()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Start client to connect to Dots and Boxes server')
    parser.add_argument('host', metavar='HOST', type=str, help='Host name of the server')
    parser.add_argument('port', metavar='PORT', type=int, help='Port number of the server')
    args = parser.parse_args(argv)

    app = QtWidgets.QApplication(sys.argv)
    gui = ClientGUI(args.host, args.port)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
