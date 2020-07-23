class LedRGB{
public:

  // PINOS DOS LEDS
  const int red;
  const int green;
  const int blue;
  const int comum;

  // ESTADO DOS LEDS
  bool redState   = false;
  bool greenState = false;
  bool blueState  = false;

  // DEFINIÇÃO DE CATODO/ANODO COMUM
  bool catodo = true;

  // DEFINIÇÃO NOS PINOS ANALOGICOS
  bool analog = false;


  // CHAMADA DO CONSTRUTOR COM O COMUM ALIMENTADO NOS PINOS VCC/GND
  LedRGB(const int redPin, const int greenPin, const int bluePin){
    this->LedRGB(redPin, greenPin, bluePin, 0);
  }

  // CHAMADA DO CONSTRUTOR COM COMUM NOS PINOS LÓGICOS
  LedRGB(const int redPin, const int greenPin, const int bluePin, const int comumPin){
    this->red   = redPin;
    this->green = greenPin;
    this->blue  = bluePin;
    this->comum = comumPin;

    pinMode(redPin,   OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin,  OUTPUT);

    // XOR COM O BOOL CATODO 1^0 = 1 e 1^1 = 0 
    if (comumPin !=0 ) pinMode(comumPin, HIGH ^ this->catodo);
  }

  // ALTERAÇÃO DO TIPO DE LED PARA ANODO COMUM 
  void isAnodo(){
    this->catodo = false;
    pinMode(this->comum, HIGH ^ this->catodo);
  }

  void isAnalog(){
    this->analog = true;
  }

  // CONFIGURAÇAO DOS LEDS
  void set(bool red, bool green, bool blue){
    if (this.analog){
      redState   = analogWrite(this->red  , (red^this->catodo   )*150);
      greenState = analogWrite(this->green, (green^this->catodo )*150);
      blueState  = analogWrite(this->blue , (blue^this->catodo  )*150);
    }
    else{
      redState   = digitalWrite(this->red  , red^this->catodo   );
      greenState = digitalWrite(this->green, green^this->catodo );
      blueState  = digitalWrite(this->blue , blue^this->catodo  );
    }
  }

  void blink(bool red, bool green, bool blue, int time){
    bool keep[3] = {redState, greenState, blueState };
    
    this->set(red, green, blue);
    delay(time);
    
    this->set(keep[0], keep[1], keep[2]);
  }

};


