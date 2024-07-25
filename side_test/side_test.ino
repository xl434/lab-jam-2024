void setup() {
  // Initialize serial communication at 9600 baud rate
  Serial.begin(115200);
}

void loop() {
  // Print "A" to the serial port
  Serial.println("C");
  
  // Wait for 1 second
  delay(5000);
}
