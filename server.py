import json as js
from os import error
from users import Users
import socket,errno
import threading
import sys

#TODO add encypt message
#TODO add kick client option

class Server:

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connections = [[0 for i in range(3)] for j in range(10)]
    connections = []
    users = Users()

    def __init__(self):


        run_thread = threading.Thread(target=self.run)
        run_thread.daemon = True
        run_thread.start()
        self.menu()
    

    def handler(self,c,a):

        username = ""
        message = ""
        while True:
            #loads json object
            data = c.recv(self.buf_size)
            print(data)
            data = js.loads(data)
                
            #adds username and connect addr to users array
            if("username" in data):
                username = data["username"]
                self.users.add_user(username, c)
                print(username,str(a[0])+":"+str(a[1]),"connected")
            
            #directed messages bugged 
            if all(key in data for key in ("target","message")):
                username_to_find = str(data["target"])
                message = str(data["message"])
                print(username_to_find)
                target_ip = self.users.find_conn_by_name(username_to_find)

                #if target_ip not null senders name and message is sent to recipent
                if(target_ip != None):
                    #create json object with username of sender and message
                    data_to_send = js.dumps({"username":username,"message":message})
                    data = js.dumps(data)
                    target_ip.send(bytes(data_to_send,encoding='utf-8'))


            if not data:
                #displays disconnected client
                print(str(username),"disconnected")
                self.connections.remove(c)
                c.close()
                break
    
    def menu(self):
        print("")
        print("Commands:")
        print("1: List all clients")
        print("0: Exit")
        while True:
            i = input()
        
                
            if (i== "0"):
                self.tcp_sock.close()
                print("server closed") 
                sys.exit()

            #Lists all clients
            #TODO: Fix showing "User: 0"
            #TODO: Add the rest of the connection info by returning 2d array from get_connections()
            elif(i == "1"):
                users = self.users.get_all_usernames()
                for name in users:
                    print("User: "+str(name)) 
            else:
                print("not valid command")


    def run(self):

        #assigns server TCP ip, Port and recieving data buffer size
        tcp_ip = '127.0.0.1'
        tcp_port = 8080
        self.buf_size = 128
        
        #binds tcp socket and listens on it
        #if port in use, alt port num is used
        try :
            self.tcp_sock.bind((tcp_ip,tcp_port))
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print("port "+ str(tcp_port)+" in use, using alternative port")
                tcp_port = 10080
                self.tcp_sock.bind((tcp_ip,tcp_port))

        self.tcp_sock.listen(1)
        print('server running\n')

        while True:
            #accepts incoming connect requests 
            c,a = self.tcp_sock.accept()

            #creates new client handler thread for each connected client
            handler_thread = threading.Thread(target=self.handler,args = (c,a))
            handler_thread.daemon =True
            handler_thread.start() 
            
        


        




server = Server()




