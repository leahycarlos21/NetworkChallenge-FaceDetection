from ftplib import FTP
import requests
import time

FTP_PORT = 2121

ftp = FTP('')
ftp.connect('localhost',FTP_PORT)
ftp.login()
ftp.cwd('') #replace with your directory
ftp.retrlines('LIST')

def uploadFile():
 filename = 'amigos.jpg' #replace with your file in your home folder
 ftp.storbinary('STOR '+filename, open(filename, 'rb'))
 ftp.quit()

def downloadFile(filename):
 #filename = 'fotico.jpeg' #replace with your file in the directory ('directory_name')
 imname = "processed-"+ filename +".jpg"
 localfile = open(imname, 'wb')
 ftp.retrbinary('RETR ' + imname, localfile.write, FTP_PORT)
 ftp.quit()
 localfile.close()

def check_file(filename):
    print("Work")
    imname = "processed-"+ filename +".jpg"
    r = requests.post('http://localhost:23336/api/checkimage', json={"imname": imname})
    r.status_code
    print(r.json())
    #JSON
    y = r.json()
    print(y["status"])
    if(y["status"]):
        return True
    else:
        return False



#uploadFile()
#check_file("amigos")
downloadFile("amigos")
'''
if(check_file("amigos")):
    print("Sí existe mi rey")
    #time.sleep(5)
    downloadFile("amigos")
else:
    print("No existe mi rey :(")
'''
