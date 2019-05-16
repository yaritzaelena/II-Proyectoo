import socket 
misocket = socket.socket()
misocket.connect(('localhost',8000))

misocket.send('cliente')
respuesta = misocket.recv(1024)

misocket.close()