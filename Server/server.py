from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import os
import os.path
from os import path
import optparse
import socketserver
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
from fdlite import FaceDetection, FaceDetectionModel
from fdlite.render import Colors, detections_to_render_data, render_to_image 
from PIL import Image
import shutil
import re
import flask
from flask import request, jsonify

DIRECTORY =  os.getcwd()

host_name_http = "localhost"
port_http = 23336

################################################# FTP ##############################################
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
            newImage.save(DIRECTORY+"/processed-images/processed-"+fileName)
            shutil.move(file, DIRECTORY+"/raw-images/"+fileName)
        
        
    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        import os
        os.remove(file)

def ftpServer():
    FTP_PORT = 2121
    FTP_USER = "anonymous"
    FTP_PASSWORD = "anonymous@"

    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions.
    authorizer.add_user(FTP_USER, FTP_PASSWORD, DIRECTORY, perm='elradfmw')

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

############################################## FLASK API ###########################################
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/checkimage', methods=['POST'])
def api_check_image():
    req_JSON = request.json
    imname = req_JSON['imname']
    exists = path.exists("processed-images/"+imname)
    return jsonify({'response': "imname: "+imname,
                    'status':exists})
    




###################################################### MAIN ###############################################
if __name__ == '__main__':
    threading.Thread(target=ftpServer).start()
    threading.Thread(target=lambda: app.run(host=host_name_http, port=port_http, debug=True, use_reloader=False)).start()