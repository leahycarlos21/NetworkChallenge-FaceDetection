from ftplib import FTP


FTP_PORT = 2121

ftp = FTP('')
ftp.connect('localhost',FTP_PORT)
ftp.login()
ftp.cwd('') #replace with your directory

ftp.retrlines('LIST')

def uploadFile():
 filename = 'fotico.jpeg' #replace with your file in your home folder
 ftp.storbinary('STOR '+filename, open(filename, 'rb'))
 ftp.quit()

def downloadFile():
 filename = 'fotico.jpeg' #replace with your file in the directory ('directory_name')
 localfile = open(filename, 'wb')
 ftp.retrbinary('RETR ' + filename, localfile.write, FTP_PORT)
 ftp.quit()
 localfile.close()

uploadFile()
#downloadFile()

#pip3 install pyftpdlib
