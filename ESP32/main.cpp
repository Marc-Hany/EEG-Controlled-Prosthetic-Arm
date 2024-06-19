#include <ESP32Servo.h>
#include "BluetoothSerial.h"

// 180 fingers closed 0 opened
// 0 wrist normal 90 wrist rotated (handshake)
#define SERVO_PIN_wrist 14 
#define SERVO_PIN_thumb 25
#define SERVO_PIN_inpin 26
#define SERVO_PIN_inmid 27  
#define SERVO_PIN_elbow 13
#define B1 15 //orange
#define B2 4  //yellow
#define B3 5  //green
#define B4 18 //blue
#define B5 19 //purple
#define LED_PIN 23 //white
#define speed 3

int B1_state=0;
int B2_state=0;
int B3_state=0;
int B4_state=0;
int B5_state=0;
int received;
//int window_number;
int ElbowPosition;

BluetoothSerial SerialBT;

Servo servo_wrist;  // create servo object to control a servo
Servo servo_thumb;  // create servo object to control a servo
Servo servo_inmid;  // create servo object to control a servo
Servo servo_inpin;  // create servo object to control a servo
Servo servo_elbow;  // create servo object to control a servo

void Elbow_motion(int start, int end);
void Scenario_1(); // wrist rotation and fingers
void Scenario_2(); //elbow motion
void HandShake(); //handshake scenario
void Graspandlift(); 
void GUI(); //goes to Bluetooth mode

void Hand_start();
void First_digital();
void both_start();
void Lift_off();
void Replace();
void Both_released();

void setup() {
  // put your setup code here, to run once:
  servo_wrist.attach(SERVO_PIN_wrist);  
  servo_thumb.attach(SERVO_PIN_thumb);  
  servo_inmid.attach(SERVO_PIN_inmid);  
  servo_inpin.attach(SERVO_PIN_inpin);  
  servo_elbow.attach(SERVO_PIN_elbow);
  servo_wrist.write(0);
  servo_inpin.write(180);
  servo_inmid.write(180);
  servo_thumb.write(180);
  servo_elbow.write(180);
  pinMode(B1, INPUT);  
  pinMode(B2, INPUT);  
  pinMode(B3, INPUT);  
  pinMode(B4, INPUT);  
  pinMode(B5, INPUT);  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN,LOW);  
  SerialBT.begin("ESP32_Karim"); // Bluetooth device name
  Serial.begin(9600);
  Serial.println("Done initializing");

  ElbowPosition = 180;

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED_PIN,HIGH);
  B1_state=digitalRead(B1);
  B2_state=digitalRead(B2);
  B3_state=digitalRead(B3);
  B4_state=digitalRead(B4);
  B5_state=digitalRead(B5);
  if(B1_state==1)
  {
    digitalWrite(LED_PIN,LOW);
    Scenario_1();
  }
  else if(B2_state==1)
  {
    digitalWrite(LED_PIN,LOW);
    Scenario_2();
  }
  else if(B3_state==1)
  {
    digitalWrite(LED_PIN,LOW);
    HandShake();
  }
  else if(B4_state==1)
  {
    digitalWrite(LED_PIN,LOW);
    Graspandlift();
  }
  else if(B5_state==1)
  {
    digitalWrite(LED_PIN,LOW);
    GUI();
  }
  else{}

}


void Elbow_motion(int start, int end) // 180 down  and 90 up
{
  if(start < end)
  {
  for (int angle = start; angle <= end; angle += 1) {
      servo_elbow.write(angle);   
      delay(map(speed, 1, 10, 30, 1)); 
    }
    ElbowPosition = end;
  }
  else if (end < start)
  {
    for (int angle = start; angle <= end; angle -= 1) {
      servo_elbow.write(angle);   
      delay(map(speed, 1, 10, 30, 1)); 
    }
    ElbowPosition = end;

  }
  
}


void Scenario_1()
{
  Serial.println("Scenario 1");
  for (int i=0;i<2;i++)
  {
    servo_wrist.write(90);  // Rotating the wrist to grasp position
    delay(2000);

    servo_inmid.write(0);
    delay(500);
    servo_inpin.write(0);
    delay(500);
    servo_thumb.write(0);
    delay(2000);

    servo_wrist.write(0);   // Rotating the wrist back to initial position
    delay(2000);

    servo_inpin.write(180);
    delay(500);
    servo_inmid.write(180);
    delay(500);
    servo_thumb.write(180);
    delay(2000);

  }
}

void Scenario_2()
{
  Serial.println("Scenario 2");
  Elbow_motion(ElbowPosition,120);
  delay(500);
  servo_wrist.write(90);
  delay(300);
  servo_inmid.write(0);
  delay(4000);
  servo_inpin.write(0);
  delay(200);

  servo_wrist.write(0);
  delay(200);
  servo_inmid.write(180);
  delay(200);
  servo_inpin.write(180);
  delay(200);
  
  Elbow_motion(120,180);
  delay(500);
}

void HandShake() //handshake scenario
{
  servo_wrist.write(90);
  delay(300);
  Elbow_motion(ElbowPosition,110);
  for(int i=0;i<4;i++)
  {
    Elbow_motion(110,150);
    delay(500);
    Elbow_motion(150,110);
    delay(500);
  }
  Elbow_motion(110,180);
  delay(1000);
  servo_wrist.write(0);
}

void Graspandlift()
{
  Elbow_motion(ElbowPosition,110);
  delay(500);
  servo_wrist.write(90);
  delay(500);

  servo_inmid.write(60);
  delay(500);
  servo_inpin.write(60); //grasp
  delay(500);
  servo_thumb.write(60);
  delay(1000);

  Elbow_motion(110,90); //lift
  delay(2000);
  Elbow_motion(90,110); //decend
  delay(1000);

  servo_inmid.write(180);
  delay(500);
  servo_inpin.write(180); // release
  delay(500);
  servo_thumb.write(180);
  delay(1000);

  servo_wrist.write(0);
  delay(1000);

  Elbow_motion(110,180);
  delay(500);

}

void GUI() //goes to Bluetooth mode
{
  do
  {
    if (SerialBT.available()) {
      received = SerialBT.read();
    }
    if (received == 48)
    {
      Scenario_1();
    }
    else if(received == 49)
    {
      Scenario_2();
    }
    else if(received == 50)
    {
      HandShake();
    }
    else if(received == 51)
    {
      Graspandlift();
    }
    else if(received == 52)
    {
      Hand_start();
    }
    else if(received == 53)
    {
      First_digital();
    }
    else if(received == 54)
    {
      both_start();
    }
    else if(received == 55)
    {
      Lift_off();
    }
    else if(received == 56)
    {
      Replace();
    }
    else if(received == 57)
    {
      Both_released();
    }
    else{}

    received=77;
  }while(received != 98);
    /*
    if (received == 48)
    {
      //window_number=1;
      if (SerialBT.available()) 
      {
        received = SerialBT.read();
      }
      if(received == 48)
      {
        Manual();
      }
      else if(received == 49 || received == 50 )
      {
        EEG();
      }
      received=77;
    }
    else{}*/
}


void Hand_start()
{
  servo_wrist.write(90);
  delay(500);
  Elbow_motion(ElbowPosition,180);
  delay(1000);
  Elbow_motion(180,90);
  delay(1000);
}

void First_digital()
{
  servo_wrist.write(90);
  delay(500);
  Elbow_motion(ElbowPosition,180);
  delay(1000);
  Elbow_motion(180,90);
  delay(1000);
}

void both_start()
{
  servo_inmid.write(0);
  delay(200);
  servo_inpin.write(0);
  delay(200);
  servo_thumb.write(0);
  delay(200);
}

void Lift_off()
{
  Elbow_motion(ElbowPosition,110);
  delay(1000);
  Elbow_motion(110,90);
  delay(1000);
}

void Replace()
{
  Elbow_motion(ElbowPosition,90);
  delay(1000);
  Elbow_motion(90,110);
  delay(1000);
}

void Both_released()
{
  servo_inmid.write(180);
  delay(200);
  servo_inpin.write(180);
  delay(200);
  servo_thumb.write(180);
  delay(1000);
  servo_wrist.write(0);
  delay(500);
  Elbow_motion(ElbowPosition,180);
  delay(1000);
}
