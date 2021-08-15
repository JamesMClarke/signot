import socket
import threading
import sys


#TODO start each message with username
#TODO if port is already in used use another
#TODO add encypt message
class Server:

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):

        
        run_thread = threading.Thread(target=self.run)
        run_thread.daemon = True
        run_thread.start()
        
        self.menu()
    
        #self.con, addr = self.tcp_sock.accept()

    def handler(self,c,a):

        while True:
            
            data = c.recv(self.buf_size)
            for connection in self.connections: 
                connection.send(data)


            if not data:
                #displays disconnected client
                print(str(a[0])+ str(a[1]),"disconnected")
                self.connections.remove(c)
                c.close()

                break
            #print(str(data,'utf-8'))
    
    def menu(self):
        i = input("Input: ")
        match i:
        
            case("exit"):

                self.tcp_sock.close()
                print("server closed")
                sys.exit()

            case("list-clients"):
                for connection in self.connections:
                    print(connection)



    def run(self):

        
        #creates TCP socket, assigns ip,port
        tcp_ip = '127.0.0.1'
        tcp_port = 8080

        #recieving data bugger
        self.buf_size = 30
        self.tcp_sock.bind((tcp_ip,tcp_port))
        self.tcp_sock.listen(1)
        print('server running\n')



        while True:
            
            c,a = self.tcp_sock.accept()
            connect_thread = threading.Thread(target=self.handler,args = (c,a))
            connect_thread.daemon =True
            connect_thread.start() 

            
            self.connections.append(c)
            #sends status connected signal 
            status_ok = {"status":"client connected"}
            c.send(bytes(str(status_ok),'utf-8'))

            print("\n",str(a[0])+":"+str(a[1]),"connected")


        




server = Server()



