import socket
from playsound import playsound
songs = open("SongsList.txt", "r").read().split("\n")
for i in range(len(songs)):
    songs[i].replace("\"","'")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()
client, addr = server.accept()

while True:
    client.send("Please Select Track".encode('utf-8'))
    msg = client.recv(1024).decode('utf-8')
    msg = int(msg)
    print("Now Playing \""+songs[msg]+"\"")
    client.send(("Now Playing \""+songs[msg]+"\"").encode('utf-8'))
    playsound(songs[msg])
    print("Song \""+songs[msg]+"\" Finished Playing")
    client.send(("Song \""+songs[msg]+"\" Finished Playing").encode('utf-8'))