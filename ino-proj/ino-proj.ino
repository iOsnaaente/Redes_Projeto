#define CM 28 // Constante divisor de Centimetros
#define IN 72 // Constante divisor de Polegadas 

const uint8_t VCC  = 11;
const uint8_t trig = 12;
const uint8_t echo = 13;

float lerDistancia(long int overtime){

  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  
  long int duracao = pulseIn(echo, HIGH, overtime*1000);
  
  return ( duracao / (CM * 2.0));
}

#include <Servo.h>
Servo servito;

// false = automático : true = manual 
bool processDefinition = false; 

void setup() {

  pinMode(VCC , OUTPUT);
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);  

  digitalWrite(VCC, HIGH);

  servito.attach(9);
  Serial.begin(9600);
}

void loop(){

  if (processDefinition){
    // MODO CLIENT CONTROL

  }else{
    // MODO AUTOMÁTICO
    for(int angle = 0; angle < 180; angle++){
      servito.write(angle);
      Serial.print(angle);
      Serial.print(",");
      Serial.println( (int)(lerDistancia(100)*100) );
      delay(25);
    }
  }

}


byte *readSerial(){
  
  byte *lineReadSerial;
  bytes process[5];
  // process[0] = 1º byte do número Float
  // process[1] = 2º byte do número Float
  // process[2] = 3º byte do número Float
  // process[3] = 4º byte do número Float
  // process[4] = comando de processo manual/autommático
  // process[5] = byte de parada

  int numBytesSerial;
  byte numProcess;

  if (Serial.available())
     numBytesSerial = Serial.readBytesUntill('/0', lineReadSerial, sizeof(lineReadSerial));
  
  if (sizeof(lineReadSerial>1)){
    //Client enviou um pedido de controle
    numProcess = true;

  }else{
    // Nenhum sinal vindo do Cliente, segue o processo no modo automático 
    numProcess = false;
  }

  return process;
}

byte *float2byte(float fvalue){
  // PARA GRAVAR UM FLOAT EM *BYTE
  //
  // 1 FLOAT = 4 BYTES 
  // 1 INT   = 2 BYTES
  // 1 CHAR  = 1 BYTE 
  //
  // ENTÃO
  //
  // byte *floatNum;
  // float num = 3.1415
  //
  // floatNum = (byte*)&num;
  //
  // floatNum[0] = 1º byte do float num
  // floatNum[1] = 2º byte do float num
  // floatNum[2] = 3º byte do float num
  // floatNum[3] = 4º byte do float num
  // 
  // Podemos manipular os dados em float agora :D 

  byte *cnvValue;
  cnvValue = (byte*)(&fvalue);
  return cnvValue;
}


float byte2float(byte * arrayBytes) {
    float number;
    memcpy((void *)(&number), (void *)arrayBytes, sizeof(float));
    return number;
}