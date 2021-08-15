from json import decoder
import socket
import threading
import sys
import json as js

class Client:
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def __init__(self):
        tcp_port = 8080
        tcp_ip = '127.0.0.1'
        buff_size = 1024
        alive = True


        self.tcp_sock.connect((tcp_ip,tcp_port))
        

        while alive:
            
            data = self.tcp_sock.recv(buff_size)
            data = str(data,'utf-8')
            print(data)
            data = js.loads(data)

            if ("status" in data):
                if (data['status'] == 'ok'):
                    print("connected to server")
                    input_thread = threading.Thread(target=self.send_mesg)
                    input_thread.daemon = True
                    input_thread.start()
                    
                elif(data["status"] =='fail'):
                    print("cannot connect to server")
                    sys.exit()

            if("msg" in data):
                print("message",data['msg'])

        
            #data = js.loads(data)
            #print(data['status'])
           
            
            
            if not data:
                print('cannot connect to server')
                break
            #print(str(data,'utf-8'))


        


    def send_mesg(self):
      
        while True:
            
            mesg = input()
            
            if( mesg =="exit"):
                self.tcp_sock.close()
                self.alive = False
                exit()
            json_mesg = {"mesg":mesg}
            #converts to json
            json_mesg = js.dumps(json_mesg)
            self.tcp_sock.send(bytes(json_mesg,encoding='utf-8'))


            
client = Client()