from SerialMod.Serial import * 
import socket

# USE UDP_IP = '' TO CATH ALL IPS
# USE UDP_PORT = ARBITRARY NUMBER 
UDP_IP = '127.0.0.1'
UDP_PORT = 8080

# DEFINE THE BUFFER SIZE
BUFFER_SIZE = 1024
flagReceive = 0
sock = 0

# FLAG TO SET THE UDP CONNECTION
flagReceive = False


	try:
		# CRIAÇÃO DO SOCKET - SOCK_DGRAM = UDP 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# INICIALIZAÇÃO DO SERVIDOR SOCKET
		sock.bind((UDP_IP, UDP_PORT))

		# FLAG PARA CONTROLE DE TRANSMISSÕES
		flagReceive = False

	except:
		print("Erro na criação do socket, sugiro que reinicie o processo!!!")

	data, addr = sock.recvfrom(BUFFER_SIZE)
	print("Recebido de %s : %s " %(addr, data) )
	
	#print("solicitando o angulo %s" %data)

	funcao  = b'3'
	value   = int(data)
	end     = b'\n'

	i = i+1 if i+1 < 180 else 0 

	send = pack('cic', funcao, value, end)

	comport.write(send)

	# FORMATAÇÃO DA LEITURA
	data = comport.readline()
	data = str(data).split(',')
	data[0] = data[0].replace("b'", '')
	data[-1] = data[-1].replace("\\r\\n'",'')
	
	# DEFINIÇÃO FORMAL DA LEITURA
	angulo = data[0]
	distancia = data[-1]

	# CONFIRMAÇÃO DE RECEBIMENTO
	print("Angulo = %s  :  Distancia = %s" %(angulo, distancia))
	
	# ENVIANDO A RESPOSTA DE VOLTA
	str_send = str(distancia).encode()
	sock.sendto(str_send, addr)
