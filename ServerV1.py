import socket
from playsound import playsound
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
songs = songloader()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()
client, addr = server.accept()
while True:
    client.send("Please Select Track".encode('utf-8'))
    msg = int(client.recv(1024).decode('utf-8'))
    print("Now Playing \""+songs[msg][1]+"\"")
    client.send(("Now Playing \""+songs[msg][1]+"\"").encode('utf-8'))
    playsound(songs[msg][0])
    print("Song \""+songs[msg][1]+"\" Finished Playing")
    client.send(("Song \""+songs[msg][1]+"\" Finished Playing").encode('utf-8'))