#!/usr/bin/env python3
# encoding: utf-8

import sys
import argparse
import http.server
import socketserver
import threading

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    num_clients = 0
    clients = []
    lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_close(self):
        super().handle_close()
        with RequestHandler.lock:
            RequestHandler.num_clients -= 1
            RequestHandler.clients.remove(self)

    def do_GET(self):
        if self.path == "/demo":
            self.send_response(302)
            self.send_header("Location", "/static/demo.html")
            self.end_headers()
        elif self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/static/dotsandboxes.html")
            self.end_headers()
        elif self.path == "/connect":
            with RequestHandler.lock:
                if RequestHandler.num_clients < 2:
                    RequestHandler.num_clients += 1
                    print("New client connected: {}".format(self.client_address[0]))
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b'Connected to server')
                    RequestHandler.clients.append(self)
                else:
                    self.send_error(503, "Server at full capacity")
        else:
            super().do_GET()
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length).decode('utf-8')

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.broadcast_message(message)
    
    def send_message(self, message):
        self.wfile.write(message.encode())

    def broadcast_message(self, message):
        with RequestHandler.lock:
            for client in RequestHandler.clients:
                if client != self:
                    try:
                        client.send_message(message)
                    except:
                        print("Client disconnected: {}".format(client.client_address[0]))
                        RequestHandler.clients.remove(client)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def start_server(port):
    server = ThreadedHTTPServer(("", port), RequestHandler)
    server.serve_forever()


def main(argv=None):
    parser = argparse.ArgumentParser(description='Start server to play Dots and Boxes')
    parser.add_argument('port', metavar='PORT', type=int, help='Port to use for server')
    args = parser.parse_args(argv)

    start_server(args.port)


if __name__ == "__main__":
    sys.exit(main())
