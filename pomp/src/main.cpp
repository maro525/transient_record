#include <Arduino.h>

// #include <pt.h>
#include <Queue.h>
// #define PT_WAIT(pt, timestamp, usec) PT_WAIT_UNTIL(pt, millis() - *timestamp > usec);*timestamp = millis();
// static struct pt pt1, pt2;


String recv_str;
// Queue<String> recv_signals = Queue<String>(10);

String stop_signal = "00000000";


// 100ms
int pins[8][2] = {
  {14, 15}, {16, 17}, {18, 19}, {30, 31},
  {22, 23}, {24, 25}, {26, 27}, {28, 29}
};
int pin_num = 8;

void setup()
{
  for(int i=0; i<8; i++) {
    pinMode(pins[i][1], OUTPUT);
  }
  Serial.begin(38400);

  // PT_INIT(&pt1);
  // PT_INIT(&pt2);
}

void pomp(int index, int signal){
  digitalWrite(pins[index][0], bool(signal));
  digitalWrite(pins[index][1], 0);
}

void move(String signal) {
  // if(recv_signals.IsEmpty()) { return; }

  // String next_signal;
  // if(recv_signals.front(&next_signal)){
  for(unsigned int i=0; i<8; i++) {
    String ss;
    ss = signal.charAt(i);
    if(!ss.compareTo("1")){
      pomp(i, 1);
    } else if(!ss.compareTo("0")) {
      pomp(i, 0);
    }
  }
    // Serial.print("move");
    // Serial.print("-");
    // Serial.println(next_signal);
    // recv_signals.Pop();
}

// void add_offsignal() {
  // recv_signals.Push(stop_signal);
// }


//////////////////
///////////////////

void main_work() {
  if(Serial.available() > 0) {
    recv_str = Serial.readStringUntil("n");
    Serial.println(recv_str);
    move(recv_str);
    delay(90);
    move(stop_signal);
    // recv_signals.Push(recv_str);
    // add_offsignal();
    Serial.println("Done.");
  }
}


// /////////////
// static int thread1(struct pt *pt) {
//   static unsigned long timestamp = 0;
//   PT_BEGIN(pt);
//
//   while (true) {
//     PT_WAIT(pt, &timestamp, 10);
//     read_serial();
//   }
//
//   PT_END(pt);
// }
//
// static int thread2(struct pt *pt) {
//   static unsigned long timestamp = 0;
//   PT_BEGIN(pt);
//
//   while (true) {
//     PT_WAIT(pt, &timestamp, 10);
//     move();
//   }
//
//   PT_END(pt);
// }

////////////
////////////


void loop()
{
  main_work();
}

/////////////
/////////////
