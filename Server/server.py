from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import os
import optparse
import socketserver
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
from fdlite import FaceDetection, FaceDetectionModel
from fdlite.render import Colors, detections_to_render_data, render_to_image 
from PIL import Image

class MyHandler(FTPHandler):

    def on_connect(self):
        print ("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        print("LUIS SE LA COME sent \n")
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        
        image = Image.open(str(file))
        detect_faces = FaceDetection(model_type=FaceDetectionModel.BACK_CAMERA)
        faces = detect_faces(image)
        if not len(faces):
            print('no faces detected :(')
        else:
            render_data = detections_to_render_data(faces, bounds_color=Colors.GREEN)
            newImage = render_to_image(render_data, image)
            fileName =  os.path.basename(str(file))
            newImage.save('/home/racso/NetworkChallenge-FaceDetection/Server/raw-images/' + fileName)
        
    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        import os
        os.remove(file)

def httpServer():
    HTTP_HOST = 'localhost'
    HTTP_PORT = 8000
    HANDLER = SimpleHTTPRequestHandler
    os.chdir("/home/racso/NetworkChallenge-FaceDetection/Server/")
    httpd = socketserver.TCPServer((HTTP_HOST,HTTP_PORT), HANDLER)
    httpd.serve_forever()

def ftpServer():
    FTP_PORT = 2121
    FTP_USER = "anonymous"
    FTP_PASSWORD = "anonymous@"
    FTP_DIRECTORY = "/home/racso/NetworkChallenge-FaceDetection/Server/raw-images/"

    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elradfmw')

    handler = MyHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
  #  handler.banner = "pyftpdlib based ftpd ready."

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

