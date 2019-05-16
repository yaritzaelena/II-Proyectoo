import socket

misocket = socket.socket()
misocket.bind (('localhost', 8000))
misocket.listen(5)
while True:
    conexion, addr = misocket.accept()
    conexion.send('hola')
    conexion.close()