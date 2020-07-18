from math import sin, cos, radians
import pygame
import random
import math

screen_dimensions = [20*40,20*20]
center = [screen_dimensions[0]/2, screen_dimensions[1]]

class Color:
	white =  [255, 255, 255]
	black =  [  0,   0,   0]
	gray  =  [ 75,  75,  75]
	green =  [  0, 200,   0]
	blue  =  [ 50,  50, 200]
	red   =  [200,   0,   0]
	lightGray = [200,200,200]
	
	news = {}
	
	def __init__(self):
		pass

	def newColor(self, new):
		self.news.update(new)

cor = Color()

piece_radial = []
for i in range(180):
	piece_radial.append(0)

def drawPiece(raio, angulo=[0,0], _raioMax = 250, _num=5):

	raioMax = _raioMax
	(x,y) = center
	num = _num

	angulo[0] = radians(angulo[0])
	angulo[1] = radians(angulo[1])

	xo,x1 = raio*math.cos(angulo[1]), raio*math.cos(angulo[0])
	yo,y1 = raio*math.sin(angulo[1]), raio*math.sin(angulo[0])
	xob,x1b = raioMax*math.cos(angulo[1]), raioMax*math.cos(angulo[0])
	yob,y1b = raioMax*math.sin(angulo[1]), raioMax*math.sin(angulo[0])
	
	pygame.draw.polygon(screen, cor.red, [[x,y], [x+xob,y-yob],[x+x1b,y-y1b]],0)
	pygame.draw.polygon(screen, cor.green   , [[x,y], [x+xo,y-yo],[x+x1,y-y1]],4)	
	pygame.draw.line   (screen, cor.black   , [x+xob,y-yob], [x+x1b,y-y1b],5) 
	pygame.draw.line   (screen, cor.black   , [x+xo,y-yo], [x+x1,y-y1],5) 

	prop = raioMax/num
	for i in range(1,num):
		pygame.draw.arc(screen, cor.black, [x-(i*prop),y-(i*prop), 2*(i*prop),2*(i*prop)], 0, radians(190), 1)
		x1 = raioMax*cos(radians((180/num)*i))
		y1 = raioMax*sin(radians((180/num)*i))
		pygame.draw.line(screen, cor.black, [x,y], [x+x1,y-y1], 1)


def drawRetangulo(fonte, dim = [0,0], texto="", cor = [0,0,0], enquadro=[5,5]):
	text = fonte.render(texto,2,(0,0,0))
	surface = pygame.Surface((dim[0],dim[1]))
	surface.fill(cor)
	surface.blit(text, (enquadro[0],enquadro[1]))
	border = pygame.Surface((dim[0]+2,dim[1]+2), 0)
	border.fill((0,0,0))
	border.blit(surface, (1,1))
	return border	


where = []
def drawProcessOptions(process):
	options = ['DEMO', 'REMOTO', 'AUTOMÁTICO', 'MANUAL']
	where = []
	for i in range(len(options)):
		txtOption = drawRetangulo(pygame.font.SysFont(systemFont,22), [110,30], options[i], cor.red if process is not i else cor.green)
		screen.blit(txtOption, (screen_dimensions[0]-120, 5 + 40*i))
		where.append([screen_dimensions[0]-120,  5+ 40*i])
	return where

def detectProcessOption(coord = [0,0], _where = [0,0]):
	for surface in _where:
		if coords[0] >= surface[0] and coords[0] <= surface[0]+110:
			if coords[1] >= surface[1] and coords[1] <= surface[1]+30:
				print(where.index(surface))
				return where.index(surface)
	return process

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
process = 0

while True:
	screen.fill(cor.lightGray)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()

		if pygame.mouse.get_pressed()[0]:
			coords = pygame.mouse.get_pos()
			process = detectProcessOption(coords, where)


	where = drawProcessOptions(process)

	for i in range(0,180,1):
		drawPiece(piece_radial[i], [i,i+1])
			
	pygame.display.update()
	clock.tick(60)
	
def processDEMO():
	try:
		angulo = angulo +1
		if angulo == 180:
			angulo = 0
		value = value +1
		piece_radial[angulo] = 100*cos(radians(value)) + 100*sin(radians(value)) 
	except:
		pass
