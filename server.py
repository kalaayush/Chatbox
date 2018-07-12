import sys
import socket
import select

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 9009

def chat_server():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
 
   
    SOCKET_LIST.append(s)
 
    print ("Server started : port " + str(PORT))
 
    while True:

        
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            
            if sock == s: 
                sockfd, addr = s.accept()
                SOCKET_LIST.append(sockfd)
                print ("Client (%s, %s) connected" % addr)
                 
                broadcast(s, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             
           
            else:
                
                try:
                    
                    data = sock.recv(RECV_BUFFER)
                    data = data.decode()
                    if data:
                       
                        broadcast(s, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                            
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        
                        broadcast(s, sock, "Client (%s, %s) is offline\n" % addr) 

                
                except:
                    broadcast(s, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    s.close()
    

def broadcast (s, sock, message):
    for socket in SOCKET_LIST:
        
        if socket != s and socket != sock :
            try :
                message = message.encode()
                socket.send(message)
            except :
                
                socket.close()
                
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())     
