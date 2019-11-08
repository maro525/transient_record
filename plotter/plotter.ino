
void setup() {
    motorsetup();
}

String recv_str;

#define STOP_COMMAND "a"
#define NORMAL_ROTATE_MOTOR1 "b"
#define REVERSE_MOTOR1 "c"
#define NORMAL_ROTATE_MOTOR2 "d"
#define REVERSE_MOTOR2 "e"
#define NORMAL_ROTATE_BOTH "f"
#define REVERSE_BOTH "g"

void loop() {
    if(Serial.available() > 0) {
        recv_str = Serial.readStringUntil(".");
        Serial.println(recv_str);
        handle(recv_str);
    }
}

void handle(recv_str) {
    if(!recv_str.compareTo(STOP_COMMAND)) {
        stop_motor1();
        stop_motor2();
    }
    else if(!recv_str.compareTo(NORMAL_ROTATE_MOTOR1)) {
        normal_rotate_motor1();
    }
    else if(!recv_str.compareTo(NORMAL_ROTATE_MOTOR2)) {
        normal_rotate_motr2();
    }
    else if(!recv_str.compareTo(REVERSE_MOTOR1)) {
        reverse_motor1();
    }
    else if(!recv_str.compareTo(REVERSE_MOTOR2)) {
        reverse_motor2();
    }
    else if(!recv_str.compareTo(NORMAL_ROTATE_BOTH)) {
        normal_rotate_both();
    }
    else if(!recv_str.compareTo(REVERSE_BOTH)) {
        reverse_both();
    }
}