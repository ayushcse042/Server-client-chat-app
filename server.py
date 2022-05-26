import threading  # we will be using different threads to handle multiple clients at the same time
import socket

host='127.0.0.1' #localhost(ip address of server)
port=1234 #it must be same for client and server

serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
serversocket.bind((host,port))#binds the sockets to the given ip address
serversocket.listen(5);#server gets enable for accepting connection request

clients=[] #empty list
username=[]

#Broadcast func is to send message to all clients which are connected to it
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            client.close()

    #printing message on the server
    message = message.decode("ascii")
    print(message)

#handle the msg recieved from client
def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)

        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            name=username[index]
            msg=f"{name} left the chat".encode('ascii')
            broadcast(msg)
            username.remove(name)
            break


#Receiving /listening func
def receive():
    while True: # server will be on 24X7 for accepting the connection request

        client, address=serversocket.accept()

        #Request and store username
        client.send("Username".encode('ascii'))
        name=client.recv(1024).decode('ascii')
        print(f"Accepted new connection from {str(address)}, Username:{name}")


        username.append(name)
        clients.append(client)

        #Broadcast the username
        client.send("connected to server".encode('ascii'))
        broadcast(f"{name} joined the chat!".encode('ascii'))


        thread=threading.Thread(target=handle,args=(client,)) # thread created
        thread.start() # start method to run the thread

        write_thread=threading.Thread(target=write)
        write_thread.start()

def write():
    while True:
        message=input("")
        msg=f"server: {message}"
        broadcast(msg.encode("ascii"))

print("server is in listening mode")
receive()
