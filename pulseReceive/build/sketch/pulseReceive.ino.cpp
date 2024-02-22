#include <Arduino.h>
#line 1 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.ino"
#include <C:\Program Files (x86)\Arduino\libraries\WebUSB\WebUSB.h>
#include "pulseReceive.h"

WebUSB WebUSBSerial(1 /* https:// */, "127.0.0.1:3000");

#define Serial WebUSBSerial

#line 8 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.ino"
void setup();
#line 16 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.ino"
void loop();
#line 8 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.ino"
void setup() {
    while (!Serial) { // wait until the "connect device"
        ;
    }
    
    Serial.begin(9600);
}

void loop() {
	while (true) {
        if (Serial.available()) {
            if (readSerial() == "Upload Done.") break;
        }
    }
    Serial.println("yeet");
}

