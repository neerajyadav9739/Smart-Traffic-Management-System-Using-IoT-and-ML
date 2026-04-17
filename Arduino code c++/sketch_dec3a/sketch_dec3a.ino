#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Your library syntax:
LiquidCrystal_I2C lcd(0x27, 20, 4);

// ===== LED Pins =====
int R1 = 2, Y1 = 3, G1 = 4;
int R2 = 5, Y2 = 6, G2 = 7;
int R3 = 8, Y3 = 9, G3 = 10;
int R4 = 11, Y4 = 12, G4 = 13;

int redTime = 5;
int yellowTime = 3;
int greenTime = 7;

void setup() {

  // ===== LCD Initialization (YOUR LIBRARY VERSION) =====
  lcd.begin();      // NO arguments allowed in your library
  lcd.backlight();  // Turn ON LCD backlight

  lcd.setCursor(0, 0);
  lcd.print(" SMART TRAFFIC CTRL ");
  lcd.setCursor(0, 1);
  lcd.print(" Arduino + LCD + LED ");
  delay(2000);
  lcd.clear();

  // ===== Set LED Pins =====
  int pins[] = {R1, Y1, G1, R2, Y2, G2, R3, Y3, G3, R4, Y4, G4};
  for (int i = 0; i < 12; i++) pinMode(pins[i], OUTPUT);
}

void loop() {
  controlRoad("ROAD A", R1, Y1, G1);
  controlRoad("ROAD B", R2, Y2, G2);
  controlRoad("ROAD C", R3, Y3, G3);
  controlRoad("ROAD D", R4, Y4, G4);
}

void controlRoad(String road, int R, int Y, int G) {

  // === RED ===
  digitalWrite(R, HIGH);
  digitalWrite(Y, LOW);
  digitalWrite(G, LOW);
  showLCD(road, "RED", redTime);
  countDown(redTime);

  // === YELLOW ===
  digitalWrite(R, LOW);
  digitalWrite(Y, HIGH);
  digitalWrite(G, LOW);
  showLCD(road, "YELLOW", yellowTime);
  countDown(yellowTime);

  // === GREEN ===
  digitalWrite(R, LOW);
  digitalWrite(Y, LOW);
  digitalWrite(G, HIGH);
  showLCD(road, "GREEN", greenTime);
  countDown(greenTime);
}

void showLCD(String road, String signal, int t) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(" SMART TRAFFIC CTRL ");

  lcd.setCursor(0, 1);
  lcd.print("Road: ");
  lcd.print(road);

  lcd.setCursor(0, 2);
  lcd.print("Signal: ");
  lcd.print(signal);

  lcd.setCursor(0, 3);
  lcd.print("Timer: ");
  lcd.print(t);
}

void countDown(int sec) {
  for (int i = sec; i > 0; i--) {
    lcd.setCursor(7, 3);
    lcd.print("   ");   // clear old digits
    lcd.setCursor(7, 3);
    lcd.print(i);
    delay(1000);
  }
}
