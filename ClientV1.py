import socket
def errorSolver(ermsg):
    Error = True
    nonError = 0
    while Error:
        if "Error: " in ermsg:
            client.send(input((ermsg + "\n> ")).encode('utf-8'))
            ermsg = client.recv(8192).decode('utf-8')
        elif nonError <= 2:
            nonError += 1
        elif nonError > 2:
            Error = False
    return ermsg
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
while True:
    print(client.recv(8192).decode('utf-8'))
    client.send(input("Message: ").encode('utf-8'))
    msg = (client.recv(8192).decode('utf-8'))
    if "|-------------------------" in msg:
        print(msg)
        client.send(input("Message: ").encode('utf-8'))
        msg = (client.recv(1024).decode('utf-8'))
    if "Error: " in msg:
        msg = errorSolver(msg)
    print(msg)
    print(client.recv(8192).decode('utf-8'))