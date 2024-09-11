#include<EEPROM.h> // Khai báo thư viện EEPROM - Save as dữ liệu không mất khi tắt nguồn
#define Processed_Switch_1 3 // chân kỹ thuật số trên Arduino uno3 được sử dụng như một công tắc hành trình
#define Processed_Switch_2 4
#define BUTTON_UP 5
#define BUTTON_DOWN 7
#define  rainSensor  6  // chân tín hiệu cảm biến mưa ở chân digital 6
#define IN3 9               // chân kỹ thuật số dùng để điều khiển động cơ - L298N -Motor
#define IN4 10

void setup(){
  // Thiết đặt pin các chân số là đầu vào hay đầu ra và khởi đông giao tiếp nối tiếp
  Serial.begin(9600);                           // Open cổng Serual ở mức 9600 - Có thay đổi cho phụ hợp
  pinMode(rainSensor ,INPUT);         //Thiếp đặt pin chân cảm biến mưa (rainSensor) là INPUT 
  pinMode(IN3,OUTPUT);                 // Thiếp đặt pin chân kỹ tuật số 3 cho điều khiển động cơ DC là OUTPUT 
  
pinMode(IN4,OUTPUT);    //Thiếp đặt pin chân kỹ tuật số 4 cho điều khiển động cơ DC là OUTPUT
  pinMode(Processed_Switch_1,INPUT);    //Thiết đặt pin cho công tắc hành trình 1 và 2 là INPUT
  pinMode(Processed_Switch_2,INPUT);    // pin ấy có trở kháng cao (không cho dòng điện đi ra)
  Serial.println("Program started");             // In lên màn hình dòng chữ Đã Khởi Động Chương trình
   pinMode(BUTTON_UP,INPUT_PULLUP);
  pinMode(BUTTON_DOWN,INPUT_PULLUP);
}
void value_1_UP(){    //Hàm dùng để điều khiển động cơ với tốc độ trong khoảng 10 -1024 
  int speed = Serial.parseInt();           // hàm parsenInt trả về và dừng quá trình motor quay (1000mili,10,1024)
  int speedInput = constrain(speed,10,1024);      // consts nằm trong khoảng 10 - 1024
  analogWrite(IN3,speed);         //Lệnh xuất ra từ chân điều khiển L298N - IN3 trong khoảng 10-1024 tương tươn 10%-100%
  digitalWrite(IN4,0);         //tắt motor khi về low
  }
void value_1_DOWN(){
  int speeds = Serial.parseInt();
  int speedsInput = constrain(speeds,10,1024); //Giới hạn giá trị sensVal trong khoảng [10,1024]
      analogWrite(IN4,1024 -speeds); 
      digitalWrite (IN3 ,0);
}
void value_2_up(){
  //Thiết lập động cơ DC đảo ngược cho bộ điều khiện motor - cho phép kiểm soát hướng quay
  digitalWrite(IN4,HIGH);// Đặt chân IN4 thành mức cao (HIGH)
  digitalWrite(IN3,0);// Đặt chân IN3 thành mức thấp (LOW)
}

void value_2_down(){
  //Thiết lập động cơ DC đảo ngược cho bộ điều khiện motor - quay hướng ngược lại
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,0); 
}
void value_2_Stop(){
  //Dừng động cơ DC
  digitalWrite(IN3,0);                // IN3 và IN4 đều được đặt thành mức thấp (LOW), động cơ sẽ dừng lại
  digitalWrite(IN4,0);
}
void loop() {
  // đọc tín hiệu từ cảm biến mưa và hai công tắc
  int value = digitalRead(rainSensor);                                            // đọc tín hiệu rainSensor
  int congtac1_A = digitalRead(Processed_Switch_1 );               // Đọc tín hiệu từ công tắc 1
  int congtac2_A = digitalRead(Processed_Switch_2 );              // Đọc tín hiệu từ công tắc 2
  int chrainSensor_C  = digitalRead(rainSensor);                      // Đọc lại tín hiệu từ cảm biến mưa
  Serial.println(congtac1_A);                                             // In tín hiệu từ công tắc 1 ra cổng Serial
  Serial.println(congtac2_A);                                           // In tín hiệu từ công tắc 2 ra cổng Serial
  int valueup_Y = digitalRead(BUTTON_UP);
  int valuedown_X =digitalRead(BUTTON_DOWN);
  if(valuedown_X==0 && valueup_Y!=0 &&congtac2_A !=1 ){
  value_1_DOWN ();                                     // Nếu công tắc 2 không hoạt động hoặc công tắc 1 hoạt động, động cơ sẽ quay ngược.
}
else if(valuedown_X!=0 && valueup_Y==0 && congtac1_A !=1)
{
  value_1_UP();                            // Nếu công tắc 2 hoạt động hoặc công tắc 1 không hoạt động, động cơ sẽ quay thuận.
}
  else value_2_Stop();
           // Nếu không có điều kiện nào được thỏa mãn, động cơ sẽ dừng lại.

if(chrainSensor_C ==0 && congtac2_A!=1 )                           // Nếu không mưa và cửa đang mở
{
  Serial.println("rain will lose door");                                     // In thông báo "rain will lose door"
  value_1_DOWN ();                                                          // Động cơ quay ngược
  value_2_up(); // Động cơ quay thuận
}
else if(chrainSensor_C  ==1 && congtac1_A !=1  ) // Nếu có mưa và cửa đang đóng
{
  Serial.println("no rain will open  door");         // In thông báo "no rain will open  door"
  value_1_UP();                 // Động cơ quay thuận
  value_2_down();            // Động cơ quay ngược
}
value_1_UP ();          // Động cơ quay thuận
}
