import socket
from playsound import playsound
import os
def songloader():
    songs = open("SongsList.txt", "r").read().split("\n")
    flag = False
    flaga = "\\"
    flagb = "."
    z = []
    for x in range(0, len(songs)):
        z.append([songs[x], ""])
    for x in range(0, len(songs)):
        flagMax = 0
        flagCounter = 0
        for p in range(0, len(songs[x])):
            if songs[x][p] == flaga:
                flagMax += 1
        for y in range(0, len(songs[x])):
            if songs[x][y] == flaga and not flagCounter == flagMax:
                flagCounter += 1
            if songs[x][y] == flaga and flagCounter == flagMax:
                flag = True
                continue
            elif songs[x][y] == flagb:
                flag = False
                continue
            elif flag:
                z[x].insert(1, z[x][1] + songs[x][y])
                z[x].pop(2)
    for i in range(len(z)):
        z[i][0] = z[i][0].replace("\"", "")
    return z
trackValid = False
songs = songloader()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()
client, addr = server.accept()
while True:
    try:
        trackValid = False
        NumberValid = False
        client.send("Please Select Track".encode('utf-8'))
        while not NumberValid:
            try:
                msg = int(client.recv(1024).decode('utf-8'))
                NumberValid = True
            except:
                client.send("Error: Please enter a number".encode('utf-8'))
        while not trackValid:
            try:
                assert(os.path.isfile(songs[msg][0]))
                print("Now Playing \"" + songs[msg][1] + "\"")
                client.send(("Now Playing \""+songs[msg][1]+"\"").encode('utf-8'))
                playsound(songs[msg][0])
                print("Song \"" + songs[msg][1] + "\" Finished Playing")
                client.send(("Song \"" + songs[msg][1] + "\" Finished Playing").encode('utf-8'))
                trackValid = True
            except:
                errmsg = "Error: Failed to play track " + str(msg)
                print(errmsg)
                client.send((errmsg+"\nPlease re-select").encode('utf-8'))
                msg = int(client.recv(1024).decode('utf-8'))
    except:
        server.listen()
        client, addr = server.accept()