/*
  Office Pulse — representative single-room circuit (Work Room 1: 1 fan + 1 light shown)

  What this simulates:
  - GPIO25 drives the "Light 1" indicator LED   (stand-in for a relay->bulb channel)
  - GPIO26 drives the "Fan 1" indicator DC motor (stand-in for a relay->fan channel)
  - GPIO27 reads a pushbutton wired with an external pull-down resistor,
    representing someone flipping the physical wall switch -- the firmware
    needs to know about that, not just commands coming from the backend.
  - GPIO34 (ADC1_CH6, input-only pin) reads a potentiometer as a stand-in for
    an analog current-sense signal (a real deployment would use an ACS712 or
    an SCT-013 clamp-on CT sensor here instead; Wokwi has no such part, so a
    pot is the closest available way to demo "an analog reading exists").

  Real-hardware note (see ../README.md for the full explanation + pin table):
  in an actual office deployment, GPIO25/26 would drive a relay module's
  trigger pin, NOT the mains load directly -- the relay is what provides
  galvanic isolation between low-voltage ESP32 logic and the mains-voltage
  fan/light circuit. This sketch drives the LED/motor directly because
  that's what's being simulated in Wokwi to represent "the load turned on."

  Networking is intentionally left as a stub: wiring this ESP32 to the real
  FastAPI backend would mean adding WiFi + an HTTP POST (or MQTT publish) of
  the same JSON shape the simulator already produces, so the backend
  couldn't tell the difference between simulated and real device data.
*/

const int PIN_LIGHT1   = 25;
const int PIN_FAN1     = 26;
const int PIN_BUTTON   = 27;
const int PIN_CURRENT_SENSE = 34;  // ADC1_CH6, input-only on most ESP32 boards

unsigned long lastToggleMs = 0;
const unsigned long TOGGLE_INTERVAL_MS = 5000;  // demo-only auto-cycle
bool lightOn = false;
bool fanOn = false;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LIGHT1, OUTPUT);
  pinMode(PIN_FAN1, OUTPUT);
  pinMode(PIN_BUTTON, INPUT);       // external pull-down resistor is on the board
  // PIN_CURRENT_SENSE needs no pinMode() call for analogRead() on ESP32.

  digitalWrite(PIN_LIGHT1, LOW);
  digitalWrite(PIN_FAN1, LOW);
}

void loop() {
  bool manualOverride = digitalRead(PIN_BUTTON) == HIGH;

  // Demo-only: auto-cycle the light/fan periodically so the simulation is
  // visibly "live" without needing to click the button every time.
  if (millis() - lastToggleMs > TOGGLE_INTERVAL_MS) {
    lightOn = !lightOn;
    fanOn = !fanOn;
    lastToggleMs = millis();
  }

  // A manual press forces both on, overriding the auto-cycle -- mirroring
  // "someone at the wall switch always wins."
  if (manualOverride) {
    lightOn = true;
    fanOn = true;
  }

  digitalWrite(PIN_LIGHT1, lightOn ? HIGH : LOW);
  digitalWrite(PIN_FAN1, fanOn ? HIGH : LOW);

  int rawAdc = analogRead(PIN_CURRENT_SENSE);           // 0-4095 on ESP32
  float simulatedAmps = (rawAdc / 4095.0) * 5.0;         // arbitrary demo scaling

  Serial.print("{\"light1\":");
  Serial.print(lightOn ? "true" : "false");
  Serial.print(",\"fan1\":");
  Serial.print(fanOn ? "true" : "false");
  Serial.print(",\"manual_override\":");
  Serial.print(manualOverride ? "true" : "false");
  Serial.print(",\"current_sense_amps\":");
  Serial.print(simulatedAmps, 2);
  Serial.println("}");

  delay(500);
}
