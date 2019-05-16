import socket 


class Network :

    def  __init__ ( self ):
        self.client = socket.socket (socket. AF_INET , socket. SOCK_STREAM )
        self.host =  " 192.168.0.7 "  # Para que esto funcione en su máquina, debe ser igual a la dirección ipv4 de la máquina que ejecuta el servidor
                                    # Puede encontrar esta dirección escribiendo ipconfig en CMD y copiando la dirección ipv4. De nuevo, estos deben ser los servidores.
                                    # dirección ipv4. Este feild será el mismo para todos sus clientes.
        auto.port =  5555            
        self.addr = ( self .host, self .port)
        self.id =  self .connect ()

    def  conectar ( auto ):
        self .client.connect ( self .addr)
        return  self .client.recv ( 2048 ) .decode ()

    def  enviar ( auto , datos ):
        """
        :param data: str
        :return: str
        """
        try :
            self.client.send ( str .encode (datos))
            respuesta =  self .client.recv ( 2048 ) .decode ()
            return respuesta
        except socket.error as e:
            return  str (e)
