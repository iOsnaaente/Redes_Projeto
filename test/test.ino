#define CM 28 // Constante divisor de Centimetros
#define IN 72 // Constante divisor de Polegadas 

// DEFINIÇAO DE PROCESSO
#define MANUAL  1
#define AUTO    0
#define REMOTO -1 

// PINOS DO ULTRASSONICO
const int VCCS = 3;
const int TRIG = 4;
const int ECHO = 5;
const int GNDS = 6;

// PINOS DO POTENCIOMETRO
const int GNDP  = A4;
const int SINAL = A6;

// PINOS DOS LEDS
const int LED_Verm = A3;
const int LED_Amar = A2;
const int LED_Verd = A1;
const int LED_Comu = A0;

// BOTÃO 
const int BOT = 2;

// VARIVEIS DE CONTROLE
float distancia = 0;
float angulo    = 0;

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
  
  // PARA INICIAR O SERIAL 
  Serial.begin(9600);

}

int processDefinition = AUTO;

void loop(){
    
  long int tempoCorrido = millis();

  byte * serialReadArray = readSerial();

  if (processDefinition == REMOTO){
    // MODO REMOTO - ANGULO PEGO ATRAVES DO SERIAL
    angulo = serialReadArray[1];
    LedsConfig(0,1,0);
  
  }else if (processDefinition == MANUAL){                 
    // MODO MANUAL - POTENCIOMETRO GIRANDO MANUALMENTE
    angulo = map(analogRead(SINAL), 0, 1023, 0, 180);
    LedsConfig(1,0,0);
  
  }else if (processDefinition == AUTO){
    // MODO AUTOMTICO - LAÇO DE REPETIÇAO FOR
    angulo > 180 ? angulo = 0 : angulo++;
    LedsConfig(0,0,1);
  }

  Serial.print(angulo);
  Serial.print(",");
  Serial.println(lerDistancia(100));
  delay(25);
  
  // PARA O PROCESSO LEVAR APENAS 1 SEGUNDO FAZEMOS A COMPENSAÇAO 
  long int tempoCompensado = millis() - tempoCorrido;
  delay(1000 - tempoCompensado);
}


// BOTAO DE EMERGENCIA - COLOCA NO MODO MANUAL
void botEmergencia(){
  (processDefinition == MANUAL) ? processDefinition = AUTO : processDefinition = MANUAL;
}

/// READ THE SERIAL BUFFER
byte *readSerial(){
  if (Serial.available()){
    char lineReadSerial[12];
    int n = Serial.readBytesUntil('F', (char*)lineReadSerial, sizeof(lineReadSerial));
    
    if (n > 0){
      for(int i =0 ; i<n; i++){
        Serial.print((char)lineReadSerial[i]);
        Serial.println();
      }
      return (byte *)lineReadSerial;
    }else{
      return 0;
    }
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

// CONFIGURAÇAO DOS LEDS
void LedsConfig(bool ledVerm, bool ledAmar, bool ledVerd){
  ledVerm ? analogWrite(LED_Verm, 180) : analogWrite(LED_Verm, 0);
  ledAmar ? analogWrite(LED_Amar, 180) : analogWrite(LED_Amar, 0);
  ledVerd ? analogWrite(LED_Verd, 180) : analogWrite(LED_Verd, 0);
}

