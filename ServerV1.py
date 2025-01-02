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
def openingmsg(song):
    i = str(len(song))
    send = ('''
    -----------------------------------------------------
    |               Please Select Track                 |
    |              Tracks between 0-'''+i+'''                 |
    | enter "show all tracks" to give all track titles  |
    |            Juke box                               |
    |                - Sebation Price                   |
    -----------------------------------------------------
    ''')
    return str(send)
def showall(song):
    thelist = "|-------------------------\n"
    for i in range(len(song)):
        add = str(song[i][1])
        thelist += "|"+add+"\n"
    thelist += "| Please Select a track\n"
    thelist += "|-------------------------"
    return thelist
trackValid = False
songs = songloader()
allsongs = showall(songs)
send = openingmsg(songs)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()
client, addr = server.accept()
print("server connected")
while True:
    try:
        trackValid = False
        NumberValid = False
        first = True
        client.send(send.encode('utf-8'))
        while not NumberValid:
            try:
                msg = (client.recv(1024).decode('utf-8'))
                if msg == "show all tracks" and first:
                    client.send(allsongs.encode('utf-8'))
                    first = False
                    msg = int(client.recv(1024).decode('utf-8'))
                else:
                    msg = int(msg)
                NumberValid = True
            except ValueError:
                print("")
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
            except AssertionError:
                errmsg = "Error: Failed to play track " + str(msg)
                print(errmsg)
                client.send((errmsg+"\nPlease re-select").encode('utf-8'))
                NumberValid = False
                while not NumberValid:
                    try:
                        msg = (client.recv(1024).decode('utf-8'))
                        if msg == "show all tracks" and first:
                            client.send(allsongs.encode('utf-8'))
                            first = False
                            msg = int(client.recv(1024).decode('utf-8'))
                        else:
                            msg = int(msg)
                        NumberValid = True
                    except ValueError:
                        client.send("Error: Please enter a number".encode('utf-8'))
    except ConnectionAbortedError:
        print("ConnectionAborted\nWaiting for new client...")
        server.listen()
        client, addr = server.accept()