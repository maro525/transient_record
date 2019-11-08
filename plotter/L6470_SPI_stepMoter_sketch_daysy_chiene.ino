/*デイジーチェン接続 
Arduino11番ピン（MOSI）- 6番ピン(SDI) L6470(一台目) 3番ピン(SDO) - (SDI)L6470(二台目)(SDO) - 12番ピン（MISO) Arduino
SCK 共通
SS - CS共通
*/
#include <SPI.h>
#include <MsTimer2.h>
#include <stdio.h>

// ピン定義。
#define PIN_SPI_MOSI 11
#define PIN_SPI_MISO 12
#define PIN_SPI_SCK 13
#define PIN_SPI_SS 10
#define PIN_BUSY 9
#define PIN_BUSY2 8

void motorsetup()
{
  delay(1000);
  pinMode(PIN_SPI_MOSI, OUTPUT);
  pinMode(PIN_SPI_MISO, INPUT);
  pinMode(PIN_SPI_SCK, OUTPUT);
  pinMode(PIN_SPI_SS, OUTPUT);
  pinMode(PIN_BUSY, INPUT_PULLUP);
  pinMode(PIN_BUSY2, INPUT_PULLUP);
  SPI.begin();
  SPI.setDataMode(SPI_MODE3);
  SPI.setBitOrder(MSBFIRST);
  Serial.begin(38400);
  digitalWrite(PIN_SPI_SS, HIGH);

  L6470_resetdevice();  //1台目のL6470リセット
  L6470_resetdevice2(); //2台目のL6470リセット
  L6470_setup();        //1台目のL6470を設定
  L6470_setup2();       //2台目のL6470を設定
  L6470_getstatus();    //1台目のフラグ解放
  L6470_getstatus2();   //2台目のフラグ解放

  MsTimer2::set(25, fulash); //シリアルモニター用のタイマー割り込み
  MsTimer2::start();

  delay(2000);
}

//
////1台目正転
void normal_rotate_motor1(){
  L6470_move(1,800); //1台目を正転方向に800ステップ　(現在1/4マイクロステップ設定なので、フルステップの200ステップ分になる)
  L6470_busydelay(1000); //1台目の動作終了から１秒待つ
}

////2台目逆転
void reverse_motor1() {
  L6470_move(0, 800);
  L6470_busydelay(1000);
}

////２台目正転
void normal_rotate_motor2(){
  L6470_move2(1,800);//2台目を正転方向に800ステップ　()
  L6470_busydelay2(1000);//2台目の動作終了から１秒待つ
}

void reverse_motor2() {
  L6470_move2(0, 800);
  L6470_busydelay2(300);
}

////同時正転
void normal_rotate_both() {
  for(int i=0;i<3;i++){
    L6470_move(1,800);
    L6470_move2(1,800);
    L6470_busydelay(300);
  }
}

////同時逆転
void reverse_both() {
  for(int i=0;i<3;i++){
    L6470_move(0,800);
    L6470_move2(0,800);
    L6470_busydelay(300);
  }
}

////同時　順次　正逆転
//L6470_move(1,800);
//L6470_move2(1,800);
//L6470_move(0,800);
//L6470_move2(0,800);
//L6470_move(1,800);
//L6470_move2(1,800);
//delay(3000);
//
////交互に順次動作
//for(int i=0;i<4;i++){
//L6470_move(0,200);
//L6470_busydelay(0);
//L6470_move2(0,200);
//L6470_busydelay2(0);
//}
//delay(3000);
//
////１テンポ遅れて順次動作
//L6470_move(0,200);
//L6470_busydelay(0);
//for(int i=0;i<3;i++){
//L6470_move2(0,200);
//L6470_move(0,200);
//}
//L6470_move2(0,200);
//L6470_busydelay2(0);
//delay(3000);
//
////連続回転
//L6470_run(1,0x1234);//69step/sの速度で正転
//delay(5000);
//L6470_run2(1,0x5678);//332step/sの速度で正転
//delay(6000);
//
////回転停止
void stop_motor1() {
  L6470_softstop();//1台目回転停止
}
void stop_motor2() {
  L6470_softstop2();//2台目回転停止
}
//
////指定座標に移動
// L6470_goto(0x4321);//座標0x004321に最短でいける回転方向で移動[B]
// L6470_goto2(0x8765);//座標0x008765に最短でいける回転方向で移動[B]
// L6470_busydelay(0);//　　　　　　↓
// L6470_busydelay2(3000);//２台とも動作が完了してから３秒待つ
//
// //原点座標に移動
// L6470_gohome();//座標原点；0x000000に移動[B]
// L6470_gohome2();
//
// //原点につき次第　消磁
// L6470_hardhiz();
// L6470_hardhiz2();

void L6470_setup()
{
  L6470_setparam_acc(0x30);        //[R, WS] 加速度default 0x08A (12bit) (14.55*val+14.55[step/s^2])
  L6470_setparam_dec(0x30);        //[R, WS] 減速度default 0x08A (12bit) (14.55*val+14.55[step/s^2])
  L6470_setparam_maxspeed(0x2a);   //[R, WR]最大速度default 0x041 (10bit) (15.25*val+15.25[step/s])
  L6470_setparam_minspeed(0x1200); //[R, WS]最小速度default 0x000 (1+12bit) (0.238*val[step/s])
  L6470_setparam_fsspd(0x027);     //[R, WR]μステップからフルステップへの切替点速度default 0x027 (10bit) (15.25*val+7.63[step/s])
  L6470_setparam_kvalhold(0x28);   //[R, WR]停止時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)
  L6470_setparam_kvalrun(0x28);    //[R, WR]定速回転時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)
  L6470_setparam_kvalacc(0x28);    //[R, WR]加速時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)
  L6470_setparam_kvaldec(0x28);    //[R, WR]減速時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)

  L6470_setparam_stepmood(0x02); //ステップモードdefault 0x07 (1+3+1+3bit)
}

void L6470_setup2()
{
  L6470_setparam_acc2(0x30);        //[R, WS] 加速度default 0x08A (12bit) (14.55*val+14.55[step/s^2])
  L6470_setparam_dec2(0x30);        //[R, WS] 減速度default 0x08A (12bit) (14.55*val+14.55[step/s^2])
  L6470_setparam_maxspeed2(0x2a);   //[R, WR]最大速度default 0x041 (10bit) (15.25*val+15.25[step/s])
  L6470_setparam_minspeed2(0x1200); //[R, WS]最小速度default 0x000 (1+12bit) (0.238*val[step/s])
  L6470_setparam_fsspd2(0x027);     //[R, WR]μステップからフルステップへの切替点速度default 0x027 (10bit) (15.25*val+7.63[step/s])
  L6470_setparam_kvalhold2(0x28);   //[R, WR]停止時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)
  L6470_setparam_kvalrun2(0x28);    //[R, WR]定速回転時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)
  L6470_setparam_kvalacc2(0x28);    //[R, WR]加速時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)
  L6470_setparam_kvaldec2(0x28);    //[R, WR]減速時励磁電圧default 0x29 (8bit) (Vs[V]*val/256)

  L6470_setparam_stepmood2(0x02); //ステップモードdefault 0x07 (1+3+1+3bit)
}

void fulash()
{

  long a = L6470_getparam_abspos();
  long b = L6470_getparam_speed();
  long c = L6470_getparam_abspos2();
  long d = L6470_getparam_speed2();
  char str[15];
  snprintf(str, sizeof(str), "1pos=0x%6.6X ", a);
  Serial.print(str);
  snprintf(str, sizeof(str), "1spd=0x%5.5X ", b);
  Serial.print(str);
  snprintf(str, sizeof(str), "2pos=0x%6.6X ", c);
  Serial.print(str);
  snprintf(str, sizeof(str), "2spd=0x%5.5X ", d);
  Serial.println(str);

  /* Serial.print("0x");
  Serial.print( L6470_getparam_abspos(),HEX);
  Serial.print(" 0x");
  Serial.print( L6470_getparam_speed(),HEX);
  Serial.print(" 0x");
  Serial.print( L6470_getparam_abspos2(),HEX);
  Serial.print(" 0x");
  Serial.println( L6470_getparam_speed2(),HEX);
  */
}
