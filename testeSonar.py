from math import sin, cos, radians
from SerialMod.Serial import * 
import pygame
import random
import math

screen_dimensions = [20*40,20*20]
center = [screen_dimensions[0]/2, screen_dimensions[1]]


BAUDRATE = 9600

comportList = showSerialAvailable()
comport = serial.Serial()

flagComport = False

surfaceListPorts = []

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

def drawText():
    textFonte  = pygame.font.SysFont(systemFont,30)
    textFonte15  = pygame.font.SysFont(systemFont,15)

    txtPortas = drawRetangulo(textFonte, [275,30], "Lista de portas disponíveis", cor.gray)
    screen.blit(txtPortas, (5,5))

    if flagComport is True:		
        txtConexao = drawRetangulo(textFonte15, [110,30], "Encerrar COM Port", cor.blue)
        screen.blit(txtConexao, (screen_dimensions[0]-120, screen_dimensions[1]-40))
        txtConexao = drawRetangulo(textFonte, [210,30], str(comport.name), cor.green)
    else:
        txtConexao = drawRetangulo(textFonte15, [110,30], "COM não conectada", cor.red)
        screen.blit(txtConexao, (screen_dimensions[0]-120, screen_dimensions[1]-40))
        txtConexao = drawRetangulo(textFonte, [210,30], "Porta não conectada", cor.red)
    
    screen.blit(txtConexao, (screen_dimensions[0]*2/5, 5 ))

    for num,port in enumerate(comportList):
        txtPorta = drawRetangulo(textFonte, [200,30], str(port), cor.blue)
        screen.blit(txtPorta, (5, (num+1)*30 +10))

        if [0,(num+1)*33, port] not in surfaceListPorts:
            surfaceListPorts.append([5, (num+1)*30 +10, port])
    

optionPos = []
def drawProcessOptions(process):
    options = ['DEMO', 'REMOTO', 'AUTOMÁTICO']
    optionPos = []
    for i in range(len(options)):
        txtOption = drawRetangulo(pygame.font.SysFont(systemFont,22), [110,30], options[i], cor.red if process is not i else cor.green)
        screen.blit(txtOption, (screen_dimensions[0]-120, 5 + 40*i))
        optionPos.append([screen_dimensions[0]-120,  5+ 40*i])
    return optionPos


# INICIANDO PROCESSO NO PYGAME
pygame.init()

pygame.font.init()
systemFont = pygame.font.get_default_font()

screen = pygame.display.set_mode(screen_dimensions)

pygame.display.set_caption("Teste de sensor de proximidade")
pygame.display.set_icon(pygame.image.load("./.icon.png"))

clock = pygame.time.Clock()

x,y = 0,0

angulo = 0 
raio = 0
value = 0 
process = 0

surfaceClosePort = [screen_dimensions[0]-120, screen_dimensions[1]-40]

while True:
    screen.fill(cor.lightGray)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
            if event.key == pygame.K_a:
                surfaceListPorts = []
                comportList = showSerialAvailable()

        if pygame.mouse.get_pressed()[0]:
            coords = pygame.mouse.get_pos()

            for surface in optionPos:
                if coords[0] >= surface[0] and coords[0] <= surface[0]+110:
                    if coords[1] >= surface[1] and coords[1] <= surface[1]+30:
                        angulo = 0 
                        process = optionPos.index(surface)       

            if flagComport == False:
                for surface in surfaceListPorts:
                    if coords[0] >= surface[0] and coords[0] <= surface[0]+200:
                        if coords[1] >= surface[1] and coords[1] <= surface[1]+30:    
                            print("Comport found!!")
                            comport = initSerialListening(surface[-1], BAUDRATE, 1)
                            flagComport = True
            else:
                if coords[0] >= surfaceClosePort[0] and coords[0] <= surfaceClosePort[0]+100:
                    if coords[1] >= surfaceClosePort[1] and coords[1] <= surfaceClosePort[1]+30:
                        closeSerialConnection(comport)
                        flagComport = False

    try:
        if comport.is_open is True:
            flagComport = True
        else:
            flagComport = False
    except:
        print("Erro inesperado na Comport, encerrando a porta serial!")
        flagComport = False

    if flagComport is False:
        process = 0

    #DEMO
    if process == 0:
        try:
            angulo =  angulo +1 if angulo < 180 else 0 
            piece_radial[angulo] = abs(angulo*cos(radians(angulo))) + random.randint(-20,75) if piece_radial[angulo] < 250 else 250
        except:
            pass

    # REMOTO
    elif process == 1:
        if flagComport is True:
            pass

    # AUTOMÁTICO
    elif process == 2:
        if flagComport is True:
            try:
                angulo, raio   = str(comport.readline()).split(',')
                
                angulo = angulo.split("b'")[-1]
                raio   = raio.replace("\\r\\n'", "")

                angulo = int(angulo)
                raio   = int(raio)

                piece_radial[angulo] = raio

            except:
                print("Erro na conversão dos valores da Serial")

    drawText()
    optionPos = drawProcessOptions(process)

    for i in range(0,180,1):
        drawPiece(piece_radial[i], [i,i+1])
            
    pygame.display.update()
    clock.tick(60)