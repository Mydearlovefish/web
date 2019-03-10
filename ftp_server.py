'''
ftp 文件服务器
fork server训练
'''
from socket import *
import os,sys 
import signal
import time 

#全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)
FILE_PATH = '/home/maoxin/dandan/git/'

class FtpServer(object):
    def __init__(self,connfd):
        self.connfd = connfd

    def do_list(self):
        #获取文件列表
        file_list = os.listdir(FILE_PATH)
        if not file_list:
            self.connfd.send("文件库为空".encode())
            return 
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        
        files = ""
        for file in file_list:
            if file[0] != '.' and \
                os.path.isfile(FILE_PATH+file):
                files = files + file + ','
        #将拼接好的字符串传个客户端
        self.connfd.send(files.encode())

def do_request(connfd):
    ftp = FtpServer(connfd)
    while True:
        data = connfd.recv(1024).decode()
        if data[0] == 'L':
            ftp.do_list()


#网络搭建
def main():
    #创建套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port 8888....")
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            connfd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print("服务器异常:",e)
            continue 
        print("连接客户端：",addr)

        #创建子进程
        pid = os.fork()
        if pid == 0:
            sockfd.close()
            do_request(connfd)
            os._exit(0)
        else:
            connfd.close()

if __name__ == "__main__":
    main()