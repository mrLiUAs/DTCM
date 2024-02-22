String readSerial() {
  String input = ""; 
  while (Serial.available()) { //如果有輸入 則進行紀錄
    input += Serial.readString() ;
  }
  return input;
}