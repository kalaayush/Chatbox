import sys
import socket
import select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print ('Usage : python chat_client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
     
   
    try :
        s.connect((host, port))
    except :
        print ('Not connected')
        sys.exit()
     
    print ('Connection established')
    sys.stdout.write('You >> '); sys.stdout.flush()
     
    while True:
        socket_list = [sys.stdin, s]
         
        
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                data = data.decode()
               
                if not data :
                    print ('\nDisconnected')
                    sys.exit()
                
                else:
                
                    sys.stdout.write(data)
                    sys.stdout.write('You >> '); sys.stdout.flush()     
            
            else :
                
                msg = sys.stdin.readline()
                msg = msg.encode()
                s.send(msg)
                sys.stdout.write('You >> '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())
