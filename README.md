# Projeto de Redes Industriais 

O projeto consiste na construção de um Sonar utilizando um módulo HS-SR04 em cima de um Arduino Uno.
O Arduino irá permanecer conectado ao computador por meio de uma conexão RS-232 Serial. 

O computador irá rodar o Servidor/SonarSer.py construido sem interface rodando diretamente no prompt de comando.
Para utilizar o programa, deverá ser rodado o programa Cliente/SonarCl.py que irá reproduzir uma interface visual em Pygame.

O programa Cliente só irá rodar caso o Servidor estiver rodando em segundo plano dentro da Rede Local de internet. 

# Servidor

Dentro do servidor, a primeira coisa a ser feita é selecionar a porta a qual o arduino esta conectador.

![alt text](https://github.com/iOsnaaente/Redes_Projeto/blob/master/img/PortSelect.png)

Após selecionada a porta, o servidor UDP iniciará e estará pronto para conversar com os Clientes. 

# Cliente 

O Cliente ao iniciar o programa, irá entrar no modo DEMO como mostra a figura abaixo. 
Ele não precisa estar atrelado a nenhum Servidor nesse estágio.

![alt text](https://github.com/iOsnaaente/Redes_Projeto/blob/master/img/ModoDemo.png)

Ao selecionar outros modos no canto superior Direito do programa (Remoto e Auto), o Cliente deverá certificar-se de que há Servidor, caso no haja, ele irá congelar e deverá ser reiniciado.

Os modos são: Auto e Remoto 

No modo Remoto, um Slider irá aparecer e nele poderemos controlar o angulo do sonar para fazermos a aquisição da distancia que ele atinge.

![alt text](https://github.com/iOsnaaente/Redes_Projeto/blob/master/img/Remoto.png)

No modo Auto, o angulo do sonar irá ser aumentado gradativamente de 1 até 180 graus de forma automática.

![alt text](https://github.com/iOsnaaente/Redes_Projeto/blob/master/img/RemotoAuto.png)


# Troca de mensagens 

Após a troca de mensagens se concretizar, teremos algo no terminal do Servidor parecida com isso:

![alt text](https://github.com/iOsnaaente/Redes_Projeto/blob/master/img/Serv.png)

As mensagens trocadas são:
Ouvido   : Recebido de (IP do Cliente : Porta) : Mensagem recebida
Resposta : Angulo = 'Mensagem recebida' : Distância = Bytes [ ~float ]

![alt text](https://github.com/iOsnaaente/Redes_Projeto/blob/master/img/MensagensTrocadas.png)


