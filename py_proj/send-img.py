#SERVIDOR
import socket
from PIL import Image
port = 8000
host = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Conectado a {}'.format(addr))
    with open('logo_python.png', 'r') as f:
        conn.send(f.read())
        l = f.read()
    #im = Image.open(l)
    #im.show()
        f.close()
print('Arquivo enviado')


#CLIENTE 
import socket
from PIL import Image
host = '127.0.0.1'
port = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

print("Recebendo Dados...\n")
with open('recebido.png', 'wb') as f:
        print('file opened')
        print('Recebendo dados...')
        data = s.recv(4000)
        f.write(data)
        print(data)
        print("ENVIADO")
        f.close()
with open('recebido.png', 'rb') as f:
        im = Image.open(f)
        im.show()

print('Transferência completa!!!')
s.close()
print('Conexão encerrada.')