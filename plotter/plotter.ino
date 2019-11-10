#define STOP_COMMAND "h"
#define NORMAL_ROTATE_MOTOR1 "w"
#define REVERSE_MOTOR1 "x"
#define NORMAL_ROTATE_MOTOR2 "y"
#define REVERSE_MOTOR2 "z"
#define NORMAL_ROTATE_BOTH "a"
#define REVERSE_BOTH "b"

void setup() {
    motorsetup1();
    Serial.begin(38400);
    motorsetup2();
}

String recv_str;

void loop() {
    if(Serial.available() > 0) {
        recv_str = Serial.readStringUntil(".");
        String ss;
        ss = recv_str.charAt(0);
        Serial.println(ss);
        handleserial(ss);
        Serial.println("Done.");
    }
} 

void handleserial(String rec) {
    if(!rec.compareTo(STOP_COMMAND)) {
        stop_motor1();
        stop_motor2();
    }
    else if(!rec.compareTo(NORMAL_ROTATE_MOTOR1)) {
        normal_rotate_motor1();
    }
    else if(!rec.compareTo(NORMAL_ROTATE_MOTOR2)) {
        normal_rotate_motor2();
    }
    else if(!rec.compareTo(REVERSE_MOTOR1)) {
        reverse_motor1();
    }
    else if(!rec.compareTo(REVERSE_MOTOR2)) {
        reverse_motor2();
    }
    else if(!rec.compareTo(NORMAL_ROTATE_BOTH)) {
        normal_rotate_both();
    }
    else if(!rec.compareTo(REVERSE_BOTH)) {
        reverse_both();
    }
}

