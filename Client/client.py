from ftplib import FTP
import requests
import time

IP = '192.168.1.102'
FTP_PORT = 2121

ftp = FTP('')
ftp.connect('192.168.1.102',FTP_PORT)
ftp.login()
ftp.cwd('') #replace with your directory
ftp.retrlines('LIST')


def uploadFile(filename):
 ftp.storbinary('STOR '+filename, open(filename, 'rb'))
 ftp.quit()

def downloadFile(filename):
 #filename = 'fotico.jpeg' #replace with your file in the directory ('directory_name')
 imname = "processed-"+ filename
 localfile = open(imname, 'wb')
 ftp.retrbinary('RETR ' + imname, localfile.write, FTP_PORT)
 ftp.quit()
 localfile.close()

def check_file(filename):
    print("Work")
    imname = "processed-"+ filename
    r = requests.post('http://192.168.1.102:23336/api/checkimage', json={"imname": imname})
    r.status_code
    print(r.json())
    #JSON
    y = r.json()
    print(y["status"])
    if(y["status"]):
        return True
    else:
        return False



#uploadFile("amigos.jpg")
#check_file("amigos.jpg")
downloadFile("amigos.jpg")
'''
if(check_file("amigos")):
    print("Sí existe mi rey")
    #time.sleep(5)
    downloadFile("amigos")
else:
    print("No existe mi rey :(")
'''
