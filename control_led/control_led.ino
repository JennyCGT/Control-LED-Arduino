#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX
//const char SOH = "SOH";
//const char ETX = "ETX";
const int led = 13; 
int brightness = 100;  
int brightness_scale =100;
int cont=0;
char chain;
char STX[4];
char ETX[4];
char data[2];

void setup()
{
  pinMode(led, OUTPUT);
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  mySerial.begin(115200);
  mySerial.println("Hello, world?");
  digitalWrite(led, HIGH);

}

  
void loop() {

  brightness_scale = map(brightness,0,100,0,1000);
  digitalWrite(led, HIGH);
  delayMicroseconds(brightness);     // espera un cuarto de segundo
  digitalWrite(led, LOW); // asigna el valor LOW al pin
  delayMicroseconds(100-brightness);  
  if (Serial.available()>0){
  Serial.readBytes(STX,3);
    STX[4] = 0;
    mySerial.print("String init:  ");
    mySerial.println(String(STX));  
    if(String(STX) =="STX"){
      Serial.readBytes(data,1);
      data[1]=0;
      brightness= int(data[0]);
      mySerial.print("String data:  ");
      mySerial.println(brightness);  
      Serial.readBytes(ETX,3);
      ETX[4]=0;
      mySerial.print("String finish:  ");
      mySerial.println(String(ETX));  
      
      }


    
    }
}
