// # Connection:
// #        M1 pin  -> Digital pin 4
// #        E1 pin  -> Digital pin 5
// #        M2 pin  -> Digital pin 7
// #        E2 pin  -> Digital pin 6
// #        Motor Power Supply -> Centor blue screw connector(5.08mm 3p connector)
// #        Motor A  ->  Screw terminal close to E1 driver pin
// #        Motor B  ->  Screw terminal close to E2 driver pin
// #
// # Note: You should connect the GND pin from the DF-MD v1.3 to your MCU controller. They should share the GND pins.
// #
int E1 = 30;
int M1 = 31;
int E2 = 32;
int M2 = 33;
int inputkey;
unsigned long startTimeUp = 0;
unsigned long startTimeDown = 0;
//int timer =0;
unsigned long elapsedTimeUp = 0;
unsigned long elapsedTimeDown = 0;
void setup()
{
 pinMode(M1, OUTPUT);
 pinMode(M2, OUTPUT);
 Serial.begin(9600);
}

void loop()
{
 inputkey = Serial.read();
 //timer = millis();
 if (inputkey != -1) {
   switch (inputkey) {
     case ‘w’:
       //forward
       digitalWrite(E1, HIGH);
       digitalWrite(M1, LOW);
       digitalWrite(E2, HIGH);
       digitalWrite(M2, LOW);
       startTimeUp = millis();
       break;
     case ‘e’:
       //back
       digitalWrite(E1, LOW);
       digitalWrite(M1, HIGH);
       digitalWrite(E2, LOW);
       digitalWrite(M2, HIGH);
       startTimeDown = millis();
       break;
     case ‘s’:
       //stop
       digitalWrite(E1, LOW);
       digitalWrite(M1, LOW);
       digitalWrite(E2, LOW);
       digitalWrite(M2, LOW);
       startTimeUp = 0;
       startTimeDown = 0;
       break;
   }
 }
 elapsedTimeUp = millis() - startTimeUp;
 elapsedTimeDown = millis() - startTimeDown;
 Serial.print(“elapsedTimeUp = “);
 Serial.print(elapsedTimeUp);
 Serial.print(“, “);
 Serial.print(“elapsedTimeDown = “);
 Serial.println(elapsedTimeDown);
}