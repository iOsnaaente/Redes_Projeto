/*
*  TRABALHO DE REDES INDUSTRIAIS 
 *
 *   Autor: Bruno Gabriel Flores Sampaio
 *   Data : 26/06/2020
 *
 *   Descriço: Usando um Arduino NANO, farei o  sensoriamento
 de objetos dentro de uma area limitada em 180º
 fazendo o uso de um  HC-SR04, um sensor ultra-
 Sonico. 
 O Arduino  estara conectado ao Serial  e um script
 em python fara a leitura dos dados da porta e uti-
 lizando  transmissoes via sockets UDP, fara o con-
 trole remoto ou local do sistema.
 *
 *   Primeira atualizaçao.  
 */


#include <Servo.h>

#define CM 28 // Constante divisor de Centimetros
#define IN 72 // Constante divisor de Polegadas 

// DEFINIÇAO DE PROCESSO
#define MANUAL   '1'
#define AUTO     '2'
#define REMOTO   '3'

#define BUFFER_LEN 32

// PINOS USADOS NO ARDUINO
const int TRIG  = 4;
const int ECHO  = 5;
const int POT   = A6;
const int BOT   = 2;
const int SERVO = 11;


// VARIVEIS DE CONTROLE
static byte *serialReadArray;
static byte *lineReadSerial;

byte processDefinition = AUTO;

long int tempoCompensado  = 0;
long int tempoCorrido     = 0;

long int processKeepAlive = 0;
long int processAlive     = 0;


// VARIVEIS DE INTERESSE 
float distancia = 0;
float angulo    = 0;


// DEFINIÇAO DO SERVO
Servo servito;


// INICIO DO CODIGO
void setup() {

  // PARA O SENSOR ULTRASSONICO
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  // PARA O POTENCIOMETRO
  pinMode(POT, INPUT);

  // ATTACH DO BOTÃO
  pinMode(BOT, INPUT_PULLUP);
  //attachInterrupt(0, botEmergencia, RISING);

  // PARA O SERVO
  servito.attach(SERVO);

  // PARA INICIAR O SERIAL 
  Serial.begin(9600);

}

bool flagRemoto = false;
bool flagNewCap = false;

void loop(){

  tempoCorrido = millis();

  char line[BUFFER_LEN];

  // POR QUESTÕES  DE SEGURANÇA,  O PROCESSO  REMOTO SÓ  PODE
  // SER CHAMADO CASO A DEFINIÇÃO DO PROCESSO NÃO SEJA MANUAL
  if (processDefinition != MANUAL){

    if (Serial.available()){   
      Serial.readBytesUntil('\n', (char*)line, sizeof(line));
      processDefinition = (int)line[0]; 
      if (line[0] == REMOTO ) 
        flagNewCap = true;
    }
    
    if (processDefinition == REMOTO){
      angulo             = line[1];
      processKeepAlive   = line[2] * 100;
      
      // INICIA A CONTAGEM DO TEMPO 
      if (flagRemoto == false || flagNewCap == true){
        flagRemoto         = true;
        flagNewCap         = false;
        processAlive       = millis();
      }
      
      // CONFERE O TEMPO DA COMUNICAÇÃO INATIVA
      if(processKeepAlive < (millis()-processAlive)){
        processDefinition = AUTO;
        processKeepAlive  = 0;
        processAlive      = 0;
        flagRemoto        = false;
        Serial.println("F+HELLOFELAS");
      }
    }
  }


  if (processDefinition == REMOTO){
    // MODO REMOTO - ANGULO PEGO ATRAVES DO SERIAL
    angulo = line[1];
  }
  else if (processDefinition == MANUAL){                 
    // MODO MANUAL - POTENCIOMETRO GIRANDO MANUALMENTE
    angulo = map(analogRead(POT), 0, 1023, 0, 180);
  }
  else if (processDefinition == AUTO){
    // MODO AUTOMTICO - LAÇO DE REPETIÇAO FOR
    angulo > 180 ? angulo = 0 : angulo++;
  }

  servito.write((int)angulo);
  
  Serial.print((int)angulo);
  Serial.print(',');
  //Serial.println((int)lerDistancia(100)*100);
  Serial.println((int)100);
  delay(25);

  // PARA O PROCESSO LEVAR APENAS 1 SEGUNDO FAZEMOS A COMPENSAÇAO 
  tempoCompensado = millis() - tempoCorrido;
  delay(1000 - tempoCompensado);
}

// BOTAO DE EMERGENCIA - COLOCA NO MODO MANUAL
void botEmergencia(){
  processKeepAlive = 0;
  processAlive = 0;
  (processDefinition == MANUAL) ? processDefinition = AUTO : processDefinition = MANUAL;
}


/// READ THE DISTANCE 
float lerDistancia(long int overtime){

  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long int duracao = pulseIn(ECHO, HIGH, overtime*1000);
  return ( duracao / (CM * 2.0));
}
