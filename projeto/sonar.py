import pygame
import random
import math

cor = {
	"branco"   : [255,255,255],
	"preto"    : [  0,  0,  0],
	"cinza"    : [ 75, 75, 75],
	"verde"    : [  0,200,  0],
	"azul"     : [ 50, 50,200],
	"vermelho" : [200,  0,  0]
}

screen_dimensions = [20*40,20*20]

barraVermelha = pygame.Surface([18,5])
barraVerde    = pygame.Surface([18,5])
barraPreta    = pygame.Surface([20,7])

barraVermelha.fill(cor["vermelho"])
barraVerde.fill(cor["verde"])
barraPreta.fill(cor["preto"])

center = [screen_dimensions[0]/2, screen_dimensions[1]]

pilhas =[]
for i in range(360):
	pilhas.append(0)

piece_radial = []
for i in range(180):
	piece_radial.append(0)


def plot_barras(width = 0, heigth=0):
	for i in range(0,heigth,1):
		barraPreta.blit(barraVerde, [1,1])
		screen.blit(barraPreta, [width*20,(screen_dimensions[1])-(i*7)])
	barraPreta.blit(barraVermelha, [1,1])	
	screen.blit(barraPreta,[width*20,(screen_dimensions[1])-(heigth*7)])


def catch_Dim():
	for i in range(180):
		pilhas[i] = int(100*math.sin(GtoR(i)))


def GtoR(grau):
	return grau*0.01745


def plot_Piece(raio, angulo=[0,0], cor_=0):

	(x,y) = center
	
	angulo[0] = GtoR(angulo[0])
	angulo[1] = GtoR(angulo[1])

	xo,x1 = raio*math.cos(angulo[1]), raio*math.cos(angulo[0])
	yo,y1 = raio*math.sin(angulo[1]), raio*math.sin(angulo[0])
	xob,x1b = 250*math.cos(angulo[1]), 250*math.cos(angulo[0])
	yob,y1b = 250*math.sin(angulo[1]), 250*math.sin(angulo[0])
	
	pygame.draw.polygon(screen, cor["vermelho"], [[x,y], [x+xob,y-yob],[x+x1b,y-y1b]],0)
	pygame.draw.polygon(screen, cor["verde"]   , [[x,y], [x+xo,y-yo],[x+x1,y-y1]],4)
	pygame.draw.line   (screen, cor["preto"]   , [x+xob,y-yob], [x+x1b,y-y1b],5) 
	pygame.draw.line   (screen, cor["preto"]   , [x+xo,y-yo], [x+x1,y-y1],5) 
 

from SerialShark import *

BAUDRATE = 9600

listaPortas = showSerialAvailable()
surfaceListPorts = []

flagComport = False

comport = serial.Serial()

def detectPortSelect(coords = [0,0], flag = 0):
	try:
		for surface in surfaceListPorts:
			if coords[0] >= surface[0] and coords[0] <= surface[0]+200:
				if coords[1] >= surface[1] and coords[1] <= surface[1]+30:
					print("Comport found!!")
					comport = initSerialListening(surface[-1], BAUDRATE, 1)
					return comport
		return serial.Serial()
	except:
		comport = serial.Serial()
		attPortsAvailable()

def detectPortClose(coords = [0,0], flag = 0):
	surface = [screen_dimensions[0]-110, screen_dimensions[1]-30]
	if flagComport is True:
		if coords[0] >= surface[0] and coords[0] <= surface[0]+100:
			if coords[1] >= surface[1] and coords[1] <= surface[1]+100:
				closeSerialConnection(comport)

def drawRetangulo(fonte, dim = [0,0], texto="", cor = [0,0,0], enquadro=[5,5]):
	text = fonte.render(texto,2,(0,0,0))
	surface = pygame.Surface((dim[0],dim[1]))
	surface.fill(cor)
	surface.blit(text, (enquadro[0],enquadro[1]))
	border = pygame.Surface((dim[0]+2,dim[1]+2), 0)
	border.fill((0,0,0))
	border.blit(surface, (1,1))
	return border

def drawAll():
	textFonte  = pygame.font.SysFont(systemFont,30)
	textFonte15  = pygame.font.SysFont(systemFont,15)

	txtPortas = drawRetangulo(textFonte, [275,30], "Lista de portas disponíveis", cor["cinza"])
	screen.blit(txtPortas, (5,5))

	if flagComport is True:		
		txtConexao = drawRetangulo(textFonte15, [110,30], "Encerrar COM Port", cor['vermelho'])
		screen.blit(txtConexao, (screen_dimensions[0]-120, screen_dimensions[1]-40))
		txtConexao = drawRetangulo(textFonte, [210,30], str(comport.name), cor['verde'])
	else:
		txtConexao = drawRetangulo(textFonte15, [110,30], "COM não conectada", cor['vermelho'])
		screen.blit(txtConexao, (screen_dimensions[0]-120, screen_dimensions[1]-40))
		txtConexao = drawRetangulo(textFonte, [210,30], "Porta não conectada", cor['vermelho'])
	
	screen.blit(txtConexao, (screen_dimensions[0]*2/5, 5 ))

	for num,port in enumerate(listaPortas):
		txtPorta = drawRetangulo(textFonte, [200,30], str(port), cor['azul'])
		screen.blit(txtPorta, (5, (num+1)*30 +10))

		if [0,(num+1)*33, port] not in surfaceListPorts:
			surfaceListPorts.append([5, (num+1)*30 +10, port])

def attPortsAvailable():
	surfaceListPorts = []
	listaPortas = showSerialAvailable()

pygame.init()

pygame.font.init()
systemFont = pygame.font.get_default_font()

screen = pygame.display.set_mode(screen_dimensions)

pygame.display.set_caption("Teste de sensor de proximidade")
pygame.display.set_icon(pygame.image.load("./icon.png"))

clock = pygame.time.Clock()

x,y = 0,0

angulo = 0 
raio = 0
value = 0 

while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
			if event.key == pygame.K_a:
				listaPortas = showSerialAvailable()

		if pygame.mouse.get_pressed()[0]:
			coords = pygame.mouse.get_pos()
			detectPortClose(coords, flagComport)
			comport = detectPortSelect(coords, flagComport)
	
	screen.fill(cor["branco"])
	drawAll()

	if comport.is_open is True:
		flagComport = True
		try:	
			angulo, raio = getSerialValues(comport)
			raio = raio if raio<250 else 250
			piece_radial[angulo] = raio/100
		except:
			print("ERRO NA CONVERSÃO DA SERIAL")
	else:
		flagComport = False
		try:
			angulo = angulo +1
			if angulo == 180:
				angulo = 0
			value = value +1
			piece_radial[angulo] = 100*math.cos(GtoR(value)) + 100*math.sin(GtoR(value))**2
		except:
			pass

	for i in range(0,180,1):
		plot_Piece(piece_radial[i], [i,i+1], cor["verde"])		
		if i == angulo :
			plot_Piece(piece_radial[i], [i  ,i+1], cor["vermelho"])


	pygame.display.update()
	clock.tick(60)


