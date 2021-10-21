from ftplib import FTP
import requests

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

def downloadFile():
 filename = 'fotico.jpeg' #replace with your file in the directory ('directory_name')
 localfile = open(filename, 'wb')
 ftp.retrbinary('RETR ' + filename, localfile.write, FTP_PORT)
 ftp.quit()
 localfile.close()

def check_file():
    print("Work")
    r = requests.post('http://localhost:23336/api/checkimage', json={"imname": "processed-amigos.jpg"})
    r.status_code
    print(r.json())
    #JSON
    y = r.json()
    print(y["status"]) 



uploadFile()
#downloadFile()
#check_file()