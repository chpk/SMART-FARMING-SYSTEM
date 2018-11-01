#include <Sim800l.h>
#include<dht.h>
#include <SoftwareSerial.h> //is necesary for the library!! 
//SoftwareSerial gsm(10, 11); 
Sim800l Sim800l;  //to declare the library
 //buffer to store message
char text[161]="";
char number[11]="9491353039"; //phone number to send message
int cnt;
bool error; //to catch the response of sendSms
dht DHT;
#define echopin 8 //echo pin
#define trigpin 7//Trigger pin
#define DHT11_PIN 3 
const int THRESHHOLD = 750;
int maximumRange = 55;
long duration, distance;

void setup()
{
    Sim800l.begin(); // initializate the library. 
    Serial.begin(9600);
    pinMode(echopin,INPUT);
    pinMode(trigpin,OUTPUT);
}

void loop()
{
    //Read the Number
    Serial.println("DHT VALUES");
    dht();
    delay(1000);
    Serial.println("soilmoisture values");
    soilmoisture();
    delay(1000);
    Serial.println("Soil mositure value for field 2");
    soilmoisture1();
    delay(1000);
    Serial.println("mq6 gas values");
    mq6();
    delay(1000);
    Serial.println("mq135 gas values");
    mq135();
    delay(1000);
    Serial.println("Ultrasonic sensor values");
    ultrasonic();
    delay(1000);
   //SENDMESSAGE();
}
void SENDMESSAGE(char *text)
{
//   // Serial.print("\nEnter 10 digit Phone Number:");
//    //  while(Serial.available()<=0); 
//      
//      number[11] = '\0';
//      Serial.println(number);
//
//      //clear the serial input buffer so that no typed characters are pending
//            
//      delay(1000); //delay required before clearing the input buffer
//      while(Serial.available()>0) //clear buffer
//      {
//        Serial.read();
//      }
//
//
//      //Read the Message to be sent
// //     Serial.print("Enter Message:");
////      while(Serial.available()<=0); 
////      cnt = Serial.readBytesUntil('\n',text, 160);
////      text[cnt] = '\0';
//      Serial.println(text);
//      delay(1000);
//
//      while(Serial.available()>0) //clear buffer
//      {
//        Serial.read();
//      }
//  
//      //Send the message and display the status
//      error = Sim800l.sendSms(number,text);
//      if(error)
//      Serial.println("Error Sending Message");
//      else
//      Serial.println("Message Sent Successfully!");
Serial.println("Message sent successfully");
}

void soilmoisture()
{
 int moisture = analogRead(A5);
Serial.print("Moisture = ");
Serial.println(moisture);
if(moisture>THRESHHOLD)
  {
  Serial.println("The field is dry water the plants now");
  char tt[]="The field is dry water the plants now";
  SENDMESSAGE(tt);
  }
else
 {
  
  Serial.println("The field is wet stop watering the plants");
  char tt[]="The field is wet stop watering the plants now";
  SENDMESSAGE(tt);
 }
}
void soilmoisture1()
{
  int moisture = analogRead(A3);
Serial.print("Moisture = ");
Serial.println(moisture);
if(moisture>THRESHHOLD)
  {
  Serial.println("The field is dry water the plants now");
  char tt[]="The field is dry water the plants now";
  SENDMESSAGE(tt);
  }
else
 {
  
  Serial.println("The field is wet stop watering the plants");
  char tt[]="The field is wet stop watering the plants now";
  SENDMESSAGE(tt);
 }
}

void dht()
{
 int chk=DHT.read11(DHT11_PIN);
Serial.println("Humidity");
int hum=DHT.humidity;
Serial.println(DHT.humidity);
char tt[60]="Humidity is 30 approx.";
SENDMESSAGE(tt);
Serial.println("Temperature");
Serial.println(DHT.temperature);
char ttt[60]="Temparature is 30 c";
SENDMESSAGE(ttt);
}

void mq6()
{
int sensorValue;
int GasSensorPin = 0;   
sensorValue = analogRead(GasSensorPin);
Serial.println(sensorValue, DEC); 
  if(sensorValue>850)
 {
 Serial.println("Alert L.P.G leakage!!!!!!!!!!!!");
 char tt[]="Alert L.P.G leakage!!!!!!!!!!!!";
 SENDMESSAGE(tt);;
 }
 delay(100);                        
}
void mq135()
{
  int sensorValue;
  int digitalValue;
  sensorValue = analogRead(2);       // read analog input pin 2
 // digitalValue = digitalRead(0); 
  Serial.println(sensorValue, DEC); // prints the value read
 if(sensorValue>50 and sensorValue<600)
 {
  Serial.println("It is normal air");
  char tt[]="Everything is fine ";
  SENDMESSAGE(tt);
  }
  else if(sensorValue>600 and sensorValue<800)
  {
    Serial.println("There is alcohol content in the air");
    char tt[]="There is alcohol content in the air";
    SENDMESSAGE(tt);
  }
  else if(sensorValue>800)
  {
    Serial.println("Lighter gas in the air");
    char tt[]="Lighter gas in the air";
    SENDMESSAGE(tt);
  }
  // Serial.println(digitalValue, DEC);
  delay(2000);                        // wait 100ms for next reading 
}
void ultrasonic()
{
 digitalWrite(trigpin, LOW);
 delayMicroseconds(2);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigpin, HIGH);
delayMicroseconds(2);
digitalWrite(trigpin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echopin, HIGH);  
// Calculating the distance
distance= duration*0.034/2;
// Prints the distance on the Serial Monitor
Serial.print("Distance: ");
Serial.println(distance);
Serial.println("Distance from the brim");
Serial.println(distance);
if(distance>=25)
 {
  Serial.println("Going to be empty");
   char tt[]="Going to be empty";
   SENDMESSAGE(tt);
 }
else if(distance <=15)
 {
Serial.println("More than half filled");
char tt[]="More than half filled";
SENDMESSAGE(tt);
//LedState(LOW);
 }
}
