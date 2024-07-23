
const int speakerPin = 9;  // Speaker is connected to pin 9

void setup() {
  // Nothing needed in setup for this example
}

void loop() {
  // Generate a 440 Hz tone (A4 note) for 1 second
  tone(speakerPin, 440, 1000);
  delay(1000);

  // Generate a 523 Hz tone (C5 note) for 1 second
  tone(speakerPin, 523, 1000);
  delay(1000);

  // Generate a 587 Hz tone (D5 note) for 1 second
  tone(speakerPin, 587, 1000);
  delay(1000);
  
  // Generate a 659 Hz tone (E5 note) for 1 second
  tone(speakerPin, 659, 1000);
  delay(1000);

  // Generate a 698 Hz tone (F5 note) for 1 second
  tone(speakerPin, 698, 1000);
  delay(1000);

  // Generate a 784 Hz tone (G5 note) for 1 second
  tone(speakerPin, 784, 1000);
  delay(1000);

  // Generate a 880 Hz tone (A5 note) for 1 second
  tone(speakerPin, 880, 1000);
  delay(1000);
}
