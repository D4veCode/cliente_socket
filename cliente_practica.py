import socket, base64, hashlib

class ClientSocket():
    
    HOST = '192.168.24.1'
    PORT = 10601

    def __init__(self, usr):
        self.usr = usr
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    
    def go(self):
        self.connection(self.usr)

    def connection(self, usr):
        """
        Funcionamiento del servidor
        """
        # conexion y envio de primer comando
        self.sock_tcp.connect((self.HOST, self.PORT))
        self.sock_tcp.sendall(b'helloiam {}'.format(self.usr))
        print('Esperando respuesta del servidor...')
        msg = self.sock_tcp.recv(1024)
        print(msg)

        # envio de msglen
        self.sock_tcp.send(b'msglen')
        msglen = self.sock_tcp.recv(1024)
        print(msglen)

        # socket udp para recibir el mensaje de parte del servidor
        self.sock_udp.bind(('192.168.24.42', 15006))
        self.sock_tcp.sendall(b'givememsg 15006')
        is_ok = self.sock_tcp.recv(1024)
        print('Mensaje Recibido: {}'.format(is_ok))

        # decodificacion del mensaje enviado
        msg_encoded, address = self.sock_udp.recvfrom(4096)
        self.sock_udp.close()
        msg_decoded = base64.b64decode(msg_encoded)
        msg_priv = msg_decoded.decode('utf-8')
        print('El mensaje es:\n {}'.format(msg_priv))

        # chequeo de que el mensaje fue recibido correctamente 
        md5check = hashlib.md5(msg_priv.encode('utf-8')).hexdigest()
        self.sock_tcp.sendall(b'chkmsg {}'.format(md5check))
        resp = self.sock_tcp.recv(1024)
        print('Checksum: {}'.format(resp))

        #cerrar conexion con el servidor 
        self.sock_tcp.sendall(b'bye')
        bye = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        print('Gracias por usar el cliente, {}'.format(bye))

    

if __name__ == "__main__":
    print('Hola! Bienvenido a ClientPython!')
    cliente = ClientSocket('daserrada.16')
    cliente.go()