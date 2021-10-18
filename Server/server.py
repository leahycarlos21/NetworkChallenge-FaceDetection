from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import os
import optparse
import socketserver
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading


def httpServer():
    HTTP_HOST = 'localhost'
    HTTP_PORT = 8000
    HANDLER = SimpleHTTPRequestHandler
    os.chdir("/home/leahycarlos21/Documents/TEC/II-SEM-2021/RedesDeComutadores/GitHub/NetworkChallenge-FaceDetection/Server/")
    httpd = socketserver.TCPServer((HTTP_HOST,HTTP_PORT), HANDLER)
    httpd.serve_forever()

def ftpServer():
    FTP_PORT = 2121
    FTP_USER = "anonymous"
    FTP_PASSWORD = "anonymous@"
    FTP_DIRECTORY = "/home/leahycarlos21/Documents/TEC/II-SEM-2021/RedesDeComutadores/GitHub/NetworkChallenge-FaceDetection/Server/raw-images/"

    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Optionally specify range of ports to use for passive connections.
    #handler.passive_ports = range(60000, 65535)

    address = ('localhost', FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()


if __name__ == '__main__':
    threading.Thread(target=httpServer).start()
    threading.Thread(target=ftpServer).start()

