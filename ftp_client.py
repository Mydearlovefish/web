from socket import * 
import sys 

#具体功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd = sockfd
    
    def do_list(self):
        self.sockfd.send(b'L') #发送请求
        #等待回复
        data = self.sockfd.recv(128).decode()
        if data == 'OK':
            data = self.sockfd.recv(4096).decode()
            files = data.split(',')
            for file in files:
                print(file)
        else:
            #无法完成操作
            print(data)

#网络连接
def main():
    #服务器地址
    ADDR =('127.0.0.1',8888)

    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("连接服务器失败:",e)
        return 
    
    #创建文件处理类对象
    ftp = FtpClient(sockfd)

    while True:
        print("\n=======命令选项=========")
        print("***     list        ***")
        print("***   get  file     ***")
        print("***   put  file     ***")
        print("***     quit        ***")
        print("========================")

        cmd = input("输入命令>>")
        if cmd.strip() == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            ftp.do_get()
        elif cmd[:3] == 'put':
            ftp.do_put()
        else:
            print("请输入正确命令")


if __name__ == "__main__":
    main()    


    

