# 1 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.ino"
# 2 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.ino" 2
# 3 "C:\\Users\\Stanley\\OneDrive\\桌面\\program\\arduino\\pulseReceive\\pulseReceive.ino" 2

WebUSB WebUSBSerial(1 /* https:// */, "127.0.0.1:3000");



void setup() {
    while (!WebUSBSerial) { // wait until the "connect device"
        ;
    }

    WebUSBSerial.begin(9600);
}

void loop() {
 while (true) {
        if (WebUSBSerial.available()) {
            if (readSerial() == "Upload Done.") break;
        }
    }
    WebUSBSerial.println("yeet");
}
