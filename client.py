import socket
import threading # client needs to have two threads that are running at the same time
#(one for sending the message and other one for recieving the message)

#choose username
username=input("Enter your username ")


clientsocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# SENDS THE CONNEC.REQUEST
clientsocket.connect(('127.0.0.1',1234)) # IT TAKES SINGLE ARGUMENT (TUPLE)

 

#listening to the server and sending username
def recieve():
    while True:   # endless while loop (because it continuosly tries to recieve the message and print them)
        try:
            #recieve msg from server
            #if 'Username' then send username
            message=clientsocket.recv(1024).decode('ascii') #ascii=character encoding standard for electronic communication
            if message=="Username":
                clientsocket.send(username.encode("ascii"))
            else:
                print(message)

        except:
            #close connection when error
            print("An error occured!")
            clientsocket.close()
            break


#sending messages to the server
def write():
    while True:
        message='{}:{}'.format(username,input(""))
        clientsocket.send(message.encode("ascii"))


# starting threads for listening(recieving messages) and writing
recieve_thread=threading.Thread(target=recieve)
recieve_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()
