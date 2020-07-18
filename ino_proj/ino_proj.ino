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
#define MANUAL  -1
#define AUTO     0
#define REMOTO   1 

#define BUFFER_LEN 32
#include "Led_H.h"

// PINOS DO ULTRASSONICO
const int VCCS = 3;
const int TRIG = 4;
const int ECHO = 5;
const int GNDS = 6;

// PINOS DO POTENCIOMETRO
const int GNDP  = A4;
const int SINAL = A6;

// INICIA A CLASSE LED (RED, GREEN, BLUE, COMUM) 
LedRGB led(A3,A2,A1,A0);
led.isAnalog();

// BOTÃO 
const int BOT = 2;

// PINOS SERVOS
const int SERVO = 11;

// VARIVEIS DE CONTROLE
static byte *serialReadArray;
static byte *lineReadSerial;

byte processDefinition = AUTO;

long int tempoCompensado  = 0;
long int tempoCorrido     = 0;

long int processKeepAlive = 0;
long int processAlive     = 0;

float distancia = 0;
float angulo    = 0;

// DEFINIÇAO DO SERVO
Servo servito;

// INICIO DO CODIGO
void setup() {
  
  // PARA O SENSOR ULTRASSONICO
  pinMode(VCCS, OUTPUT);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(GNDS, OUTPUT);
  digitalWrite(VCCS, HIGH);
  digitalWrite(GNDS, LOW);
  
  // PARA O POTENCIOMETRO
  pinMode(GNDP,  OUTPUT);
  pinMode(SINAL, INPUT);
  analogWrite(GNDP, 0);
  
  // ATTACH DO BOTÃO
  pinMode(BOT, INPUT_PULLUP);
  attachInterrupt(0, botEmergencia, RISING);

  // PARA O SERVO
  servito.attach(SERVO);
  
  // PARA INICIAR O SERIAL 
  Serial.begin(9600);

}


void loop(){
    
  tempoCorrido = millis();

  // POR QUESTÕES  DE SEGURANÇA,  O PROCESSO  REMOTO SÓ  PODE
  // SER CHAMADO CASO A DEFINIÇÃO DO PROCESSO NÃO SEJA MANUAL
  if (processDefinition != MANUAL){

    serialReadArray = readSerial();

    if (!serialReadArray){

      if ((processDefinition  = serialReadArray[1]) == REMOTO){
        angulo             = byte2float(serialReadArray, 2);
        processKeepAlive   = byte2float(serialReadArray, 5);
        processAlive       = millis();

      }else{
        processAlive = 0;
        processKeepAlive = 0;
        processDefinition = AUTO;
      }
    }

    // CONFERE O TEMPO DA COMUNICAÇÃO INATIVA
    if (processDefinition == REMOTO){   
      if(processKeepAlive < (millis()-processAlive)){
        processDefinition = AUTO;
        processKeepAlive  = 0;
        processAlive      = 0;
      }
    }
  }


  if (processDefinition == REMOTO){
    // MODO REMOTO - ANGULO PEGO ATRAVES DO SERIAL
    angulo = byte2float(serialReadArray, 0);
    led.set(0,1,0);
  
  }else if (processDefinition == MANUAL){                 
    // MODO MANUAL - POTENCIOMETRO GIRANDO MANUALMENTE
    angulo = map(analogRead(SINAL), 0, 1023, 0, 180);
    led.set(1,0,0);
  
  }else if (processDefinition == AUTO){
    // MODO AUTOMTICO - LAÇO DE REPETIÇAO FOR
    angulo > 180 ? angulo = 0 : angulo++;
    led.set(0,0,1);
  }

  servito.write((int)angulo);
  Serial.print(processKeepAlive);
  Serial.print(",");
  Serial.print(processDefinition);
  Serial.print(",");
  Serial.print(angulo);
  Serial.print(",");
  Serial.println( (int)(lerDistancia(100)*100) );
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


/// READ THE SERIAL BUFFER
byte *readSerial(){
  if (Serial.available()){
    char *lineReadSerial[BUFFER_LEN];
    Serial.readBytesUntil('F', (char*)lineReadSerial, sizeof(lineReadSerial));
    if (lineReadSerial[0]=='I')
      return (byte *)lineReadSerial;
    else
      return 0;
  }else{
    return 0;    
  }
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


/// FLOAT IN A ARRAY
byte* float2byte(float fvalue){
  byte *cnvValue;
  cnvValue = (byte*)(&fvalue);
  return cnvValue;
}

/// FLOAT IN A ARRAY
float byte2float(byte * byteValues, int pos) {
    float fvalue;
    byte * aux = (byte*)malloc(sizeof(float));
    for (int i =0; i <sizeof(float); i++)
      aux[i] = byteValues[pos+i];
    memcpy((void *)(&fvalue), (void *)aux, sizeof(float));
    free(aux);
    return fvalue;
}

/// ARRAY OF FLOAT - OVERWRITE
float byte2float(byte *byteValues){
    float fvalue;
    memcpy((void *)(&fvalue), (void *)byteValues, sizeof(float));
    return fvalue;
}


