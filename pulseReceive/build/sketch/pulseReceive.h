#line 1 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.h"
String readSerial() {
  String input = ""; 
  while (Serial.available()) { //如果有輸入 則進行紀錄
    input += Serial.readString() ;
  }
  return input;
}