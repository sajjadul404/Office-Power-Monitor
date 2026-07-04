# Hardware / Electrical Schematic

The spec only requires a representative circuit for one room, wired well
enough to "make physical sense" — not all 15 devices. This shows **Work
Room 1** (1 fan + 1 light, easily duplicated) with an ESP32 as the
controller.

## How to open it

1. Go to [wokwi.com/projects/new](https://wokwi.com/projects/new) and pick
   **ESP32**.
2. Replace the generated `diagram.json` and `sketch.ino` with the files in
   this folder.
3. Press ▶ to run the simulation. The LED represents Light 1, the DC motor
   represents Fan 1, the pushbutton simulates someone flipping the physical
   wall switch, and the potentiometer stands in for a current-sense reading
   (Wokwi has no ACS712/CT-clamp part, so a pot is the closest way to
   demonstrate "an analog sensing input exists" — see note below).

**Honesty note:** I'm confident about the core part types used here (ESP32
DevKit V1, LED, DC motor, pushbutton, resistor, potentiometer — all common
Wokwi library parts), but I haven't run this inside an actual Wokwi session
to confirm pixel-perfect import. If a part fails to load or a pin name is
slightly off, the Wokwi editor's autocomplete on pin names will get you the
rest of the way in under a minute — treat this as a strong starting point,
not a guaranteed-perfect one-click import.

## Wokwi simulation — pin mapping

| Function | ESP32 Pin | Component | Notes |
|---|---|---|---|
| Light 1 output | GPIO25 | LED (via 220Ω resistor) | Stand-in for a relay-driven bulb channel |
| Fan 1 output | GPIO26 | DC motor | Stand-in for a relay-driven fan channel |
| Manual wall-switch input | GPIO27 | Pushbutton (external 10kΩ pull-down) | Lets firmware detect a physical override, not just app/bot commands |
| Current-sense input | GPIO34 (ADC1_CH6) | Potentiometer wiper | Stand-in for an ACS712/SCT-013 analog reading; GPIO34 is input-only on most ESP32 boards, which is exactly the right kind of pin for a sensor |
| Common ground | GND | All components | Every module needs to share this reference or readings/outputs will be meaningless |

## What changes in a real deployment

The simulation drives the LED/motor **directly** from GPIO for simplicity.
Real hardware must not do this — a GPIO pin sources a few mA at 3.3V; a
mains light or fan draws real current at 120/230V AC. The two circuits need
to be electrically isolated. Here's the actual wiring reasoning:

| Function | ESP32 Pin | Real component | Why |
|---|---|---|---|
| Light 1 trigger | GPIO25 | Relay module IN (or solid-state relay gate) | GPIO drives the relay's low-voltage coil/trigger side only |
| Light 1 load | — | Relay COM/NO wired in-line with the mains light circuit | The relay's contacts switch the actual 120/230V AC — the ESP32 never touches mains directly |
| Fan 1 trigger | GPIO26 | Relay module IN | Same reasoning as above |
| Current sensing | GPIO34 (ADC) | ACS712 (in-line) or SCT-013 (clamp-on, non-invasive) feeding a scaled analog voltage | Gives a real measured wattage instead of the nameplate-wattage estimate the simulation uses |
| Manual override | GPIO27 | Existing wall switch, read via an opto-isolator or a second relay's dry contact | Keep the ESP32's GPIO isolated from mains — never wire a 120/230V switch leg straight into a microcontroller pin |

**Isolation is the load-bearing safety point here**, not a formality: the
relay (or SSR) is what stands between "an ESP32 GPIO glitching" and "a fan
motor or bulb glitching." Skipping it to save a component is how you burn
out a microcontroller — or worse.

## Scaling from 1 room (2 devices shown) to all 15

An ESP32 has ~25 usable GPIOs, so wiring 15 relay channels + 15 sense lines
one-to-one is tight but not impossible for a single room's 5 devices — it
falls apart at the full-office scale of 15. Two reasonable approaches:

1. **I/O expansion**: drive relays through an I2C GPIO expander (PCF8574 —
   8 channels, or MCP23017 — 16 channels) or an 8/16-channel relay board
   with its own shift register, so 2 ESP32 pins (I2C SDA/SCL) control many
   relay channels instead of 1 GPIO per relay.
2. **Per-room current sensing instead of per-device**: wiring an individual
   current sensor to every one of 15 devices is a lot of extra wiring for
   a marginal accuracy gain. Measuring total current per room (one CT clamp
   per room, at the room's sub-circuit) and using the *rated* wattage per
   device (what the simulation already does) for the breakdown is the more
   practical trade-off — call this out explicitly as a design decision if
   asked, rather than pretending per-device metering is free.

A cleaner alternative worth mentioning: Tasmota-flashed smart plugs (e.g.
Sonoff S31) already do on/off + real energy metering per outlet and talk
MQTT — for a real office retrofit that's less wiring work than building
custom relay channels for every device, at the cost of being locked into
whatever the plug's form factor supports.
