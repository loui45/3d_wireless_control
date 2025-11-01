// Arduino UNO + Joystick + Button + HC-05 Bluetooth

#define joyX A0          // Joystick X-axis
#define joyY A1          // Joystick Y-axis
#define button 2         // Button pin

// Thresholds for analog readings
#define THRESHOLD_LOW 400
#define THRESHOLD_HIGH 600

void setup() {
  Serial.begin(9600);          // Bluetooth baud rate
  pinMode(button, INPUT_PULLUP); // Button input
}

void loop() {
  int x = analogRead(joyX);
  int y = analogRead(joyY);
  bool pressed = !digitalRead(button);

  // X-axis for left/right rotation
  if (x < THRESHOLD_LOW) {
    Serial.println("ROTATE_LEFT");
  } else if (x > THRESHOLD_HIGH) {
    Serial.println("ROTATE_RIGHT");
  }

  // Y-axis for up/down rotation
  if (y < THRESHOLD_LOW) {
    Serial.println("ROTATE_UP");
  } else if (y > THRESHOLD_HIGH) {
    Serial.println("ROTATE_DOWN");
  }

  // Button controls
  if (pressed) {
    Serial.println("ROLL_LEFT");   // Example: button rolls left
    // You can add logic to toggle or send ROLL_RIGHT if needed
  }

  delay(100); // Small delay to avoid flooding Python with messages
}
