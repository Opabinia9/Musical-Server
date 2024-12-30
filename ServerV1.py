import socket
from playsound import playsound

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()

client, addr = server.accept()

while True:
    client.send("Please Select Track".encode('utf-8'))
    msg = client.recv(1024).decode('utf-8')
    print("Now Playing \"" + msg + "\"")
    client.send(("Now Playing \"" + msg + "\"").encode('utf-8'))
    playsound('C:\\Users\\sebas\\OneDrive\\Music\\new\\Billy Joel - A Matter of Trust.mp3')
    print("Song \""+msg+"\" Finished Playing")
    client.send(("Song \""+msg+"\" Finished Playing").encode('utf-8'))