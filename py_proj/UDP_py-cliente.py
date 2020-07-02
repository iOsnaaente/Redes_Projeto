import socket   
import sys      

# TENTA CRIAR O SOCKET UDP - SEMELHANTE AO DE CPP
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Failed to create socket")
    sys.exit()

host = 'localhost'
port = 8888

def sendData(msg):
    #ENVIA A SOLICITAÇÃO
    s.sendto(msg, (host, port))

    #AGUARDA A RESPOSTA
    d = s.recvfrom(1024)

    #MENSAGEM RECEBIDA
    reply = d[0]

    # 'ENDEREÇO' DA RESPOSTA 
    #addr = d[1] - não usado (já sabemos qual é)

    print ('Servidor retornou: ' + reply)
    return reply