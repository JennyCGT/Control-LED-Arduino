#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX
const int led = 13; 
int brightness = 0;  
int brightness_off = 0;  
int brightness_scale =100;
int cont=0;
char chain;
char STX[4];
char ETX[4];
char SOH[4];
char header[2];
char data[2];

void setup()
{
  pinMode(led, OUTPUT);
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  mySerial.begin(115200);
  mySerial.println("Hello, world?");

}

  
void loop() {

  digitalWrite(led, HIGH);
  delayMicroseconds(brightness);     // espera un cuarto de segundo
  digitalWrite(led, LOW); // asigna el valor LOW al pin
  delayMicroseconds(brightness_off);  

    if (Serial.available()>0){
    Serial.readBytes(SOH,3);
    SOH[4] = 0;
    if(String(SOH) =="SOH"){
      Serial.readBytes(header,1);
      header[1]=0;
      if(String(header)=="B"){
        Serial.readBytes(STX,3);
        STX[4] = 0;
        if(String(STX)=="STX"){
          Serial.readBytes(data,1);
          data[1]=0;
          brightness_off = int(data[0]);        
          mySerial.print("String data B:  ");
          mySerial.println(brightness_off);  
          }
        }
       else if(String(header)=="A"){
        Serial.readBytes(STX,3);
        STX[4] = 0;
        if(String(STX)=="STX"){
          Serial.readBytes(data,1);
          data[1]=0;
          brightness = int(data[0]);        
          mySerial.print("String data A:  ");
          mySerial.println(brightness);  
          }
        }
      Serial.readBytes(ETX,3);
      ETX[4]=0;
      Serial.flush();
        
   }
   
  }  
  
}
