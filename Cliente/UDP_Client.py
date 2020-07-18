import socket   
import sys      

# TENTA CRIAR O SOCKET UDP - SEMELHANTE AO DE CPP
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Failed to create socket")
    sys.exit()

host = 'localhost'
port = 8080

def sendData(msg):
    #ENVIA A SOLICITAÇÃO
    s.sendto(msg, (host, port))

    #AGUARDA A RESPOSTA
    d = s.recvfrom(1024)

    #MENSAGEM RECEBIDA
    reply = d[0]

    print ('Servidor retornou: ' + str(reply))
    return reply


if __name__ == "__main__":

    intState  = 1
    floatAng  = 180.0101010
    floatTime = 2.24

    strMsg = str(intState) + ':' + str(floatAng) + ':' + str(floatTime) + '\n'

    msg = bytearray(strMsg.encode())
    sendData(msg)