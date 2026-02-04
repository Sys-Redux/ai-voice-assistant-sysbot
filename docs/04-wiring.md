# SysBot Wiring Guide

## Overview

This document provides detailed wiring instructions for connecting all hardware components of the SysBot AI Voice Assistant on Wheels. Follow this guide carefully to ensure proper connections and avoid damage to components.

---

## ⚠️ Safety Warnings

1. **Always power off** the Raspberry Pi before making any connections
2. **Double-check polarity** on all power connections - reversed polarity can destroy components
3. **Never connect 12V directly to GPIO pins** - GPIO pins are 3.3V logic only
4. **Use appropriate wire gauges** - motor power wires should be at least 18-20 AWG
5. **Secure all connections** - loose wires can cause intermittent failures or shorts

---

## 📋 Components List

| Component | Quantity | Purpose |
|-----------|----------|---------|
| Raspberry Pi 5 (8GB) | 1 | Main controller |
| Raspberry Pi Zero 2 W (optional) | 1 | Dedicated motion controller |
| WM8960 Audio HAT | 1 | Audio I/O (speakers & microphone) |
| Hoysond 7" Touchscreen (1024x600) | 1 | Display for cat robot UI |
| Raspberry Pi AI Camera | 1 | Vision/person detection |
| PCA9685 I2C PWM Driver | 1 | Servo motor control |
| Cunyuer DC5 12V Dual Channel H Bridge | 1 | DC motor control |
| Geartesian DC 12V 100RPM Gear Motors | 2 | Drive motors |
| MG996R Servo Motor | 1 | Head rotation |
| 12V 5600mAh LiPo Battery Pack | 1 | Power source |
| 5V Step-Down Voltage Regulator (5A) | 1 | Pi & electronics power |

---

## 🔌 Raspberry Pi 5 GPIO Pinout Reference

```
                    3V3  (1) (2)  5V
          GPIO2/SDA (3) (4)  5V
          GPIO3/SCL (5) (6)  GND
              GPIO4 (7) (8)  GPIO14/TXD
                GND (9) (10) GPIO15/RXD
             GPIO17 (11) (12) GPIO18/PCM_CLK
             GPIO27 (13) (14) GND
             GPIO22 (15) (16) GPIO23
                3V3 (17) (18) GPIO24
   GPIO10/SPI_MOSI (19) (20) GND
    GPIO9/SPI_MISO (21) (22) GPIO25
   GPIO11/SPI_SCLK (23) (24) GPIO8/SPI_CE0
                GND (25) (26) GPIO7/SPI_CE1
      GPIO0/ID_SDA (27) (28) GPIO1/ID_SCL
              GPIO5 (29) (30) GND
              GPIO6 (31) (32) GPIO12
             GPIO13 (33) (34) GND
             GPIO19 (35) (36) GPIO16
             GPIO26 (37) (38) GPIO20
                GND (39) (40) GPIO21
```

---

## 1️⃣ WM8960 Audio HAT

The WM8960 Audio HAT is designed to sit directly on top of the Raspberry Pi's 40-pin GPIO header. It uses the I2S audio interface and I2C for control.

### Connection Method
**HAT Style (Direct Mount)** - Simply align the HAT's 40-pin header with the Pi's GPIO pins and press down firmly.

### Pass-Through Header (Important!)
The WM8960 Audio HAT has **pass-through GPIO pins** on top of the HAT. This means:
- The HAT plugs into the Pi's 40-pin header (female connector on bottom of HAT)
- Male pins stick out on **top of the HAT**, mirroring the GPIO signals
- **All other components connect to the pins on top of the Audio HAT**, not directly to the Pi

```
    ┌─────────────────────────────────────┐
    │     PINS ON TOP OF AUDIO HAT        │  ◄── Connect PCA9685, H-Bridge, etc. here
    │  (Pass-through GPIO header)         │
    ├─────────────────────────────────────┤
    │                                     │
    │         WM8960 AUDIO HAT            │  ◄── Speakers connect to terminal blocks
    │    (Microphones, audio circuits)    │
    │                                     │
    ├─────────────────────────────────────┤
    │     HAT's 40-pin female header      │  ◄── Plugs onto Pi
    └─────────────────────────────────────┘
                    │
    ┌───────────────┴───────────────────┐
    │         RASPBERRY PI 5            │
    │     (40-pin GPIO header)          │
    └───────────────────────────────────┘
```

**What this means for wiring:**
- ✅ **I2C pins (GPIO2/SDA, GPIO3/SCL)** - Available on pass-through, can be shared with PCA9685
- ✅ **Motor control pins (GPIO5, 6, 12, 13)** - Available on pass-through for H-Bridge
- ✅ **Power and Ground pins** - Available on pass-through
- ❌ **I2S Audio pins (GPIO18, 19, 20, 21)** - Reserved for audio, do not use
- ⚠️ **GPIO17** - Used by HAT's optional button, avoid if using that feature

### Pins Used by WM8960

| Function | Raspberry Pi Pin | GPIO (BCM) | Description |
|----------|-----------------|------------|-------------|
| 5V Power | Pin 2 or 4 | 5V | Power supply |
| Ground | Pin 6, 9, 14, 20, 25, 30, 34, or 39 | GND | Common ground |
| I2C Data | Pin 3 | GPIO2 (SDA) | I2C control data |
| I2C Clock | Pin 5 | GPIO3 (SCL) | I2C control clock |
| I2S Bit Clock | Pin 12 | GPIO18 | Audio bit clock |
| I2S Frame Clock | Pin 35 | GPIO19 | Audio L/R clock (LRCLK) |
| I2S Data Out (DAC) | Pin 40 | GPIO21 | Audio to speakers |
| I2S Data In (ADC) | Pin 38 | GPIO20 | Audio from microphone |
| Button (optional) | Pin 11 | GPIO17 | Custom button input |

### Speaker Wiring
The WM8960 HAT has terminal blocks for speakers:
- **LP** / **LN**: Left speaker positive / negative
- **RP** / **RN**: Right speaker positive / negative

Use 8Ω speakers (5W max per channel). Connect speaker wires to the appropriate terminals.

### Software Configuration
After mounting, install the driver:
```bash
git clone https://github.com/waveshare/WM8960-Audio-HAT
cd WM8960-Audio-HAT
sudo chmod +x install.sh
sudo ./install.sh
sudo reboot
```

---

## 2️⃣ Hoysond 7" Touchscreen Display (1024x600)

The Hoysond 7" touchscreen typically connects via **HDMI** for video and **USB** for touch input.

### Connection Method

#### Video Connection (HDMI)
- Connect the display's HDMI input to one of the Raspberry Pi 5's **micro-HDMI** ports using a micro-HDMI to HDMI cable/adapter
- Use **HDMI0** (the port closest to the USB-C power port) for primary display

#### Touch Input (USB)
- Connect the display's USB cable to any of the Raspberry Pi 5's USB ports
- The touch controller is typically plug-and-play on Raspberry Pi OS

#### Power
- Most 7" displays can be powered from the Pi's USB port
- For reliable operation, consider powering the display separately from a 5V supply

### Configuration
Add to `/boot/firmware/config.txt` if needed:
```ini
# Force HDMI output and resolution
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt=1024 600 60 3 0 0 0
```

---

## 3️⃣ Raspberry Pi AI Camera

The Raspberry Pi AI Camera connects via the **CSI (Camera Serial Interface)** port.

### Connection Method

1. **Locate the CSI port** on the Raspberry Pi 5:
   - There are two mini 22-pin CSI/DSI ports (0.5mm pitch)
   - Use **CAM0** (labeled on the board) for the primary camera

2. **Prepare the ribbon cable**:
   - The AI Camera uses a 22-pin to 15-pin adapter cable (often included)
   - Ensure the cable is the correct orientation

3. **Connect the cable**:
   - Gently pull up the plastic locking tab on the CSI connector
   - Insert the ribbon cable with the **metal contacts facing away** from the locking tab
   - The blue side of the cable typically faces towards the Ethernet port
   - Push the locking tab back down to secure

### Software Configuration
Enable the camera in Raspberry Pi OS:
```bash
sudo raspi-config
# Navigate to Interface Options → Camera → Enable
sudo reboot
```

Test the camera:
```bash
libcamera-hello
```

---

## 4️⃣ PCA9685 I2C PWM Servo Driver

The PCA9685 provides 16 channels of 12-bit PWM, perfect for controlling servos. It communicates via I2C.

### Wiring to Raspberry Pi

| PCA9685 Pin | Raspberry Pi Pin | GPIO (BCM) | Description |
|-------------|-----------------|------------|-------------|
| VCC | Pin 1 or 17 | 3.3V | Logic power (3.3V) |
| GND | Pin 6, 9, 14, 20, 25, 30, 34, or 39 | GND | Common ground |
| SDA | Pin 3 | GPIO2 (SDA) | I2C data |
| SCL | Pin 5 | GPIO3 (SCL) | I2C clock |
| V+ | External 5-6V | - | Servo power (do NOT connect to Pi) |

### ⚠️ Important Notes
- **VCC** is logic power only (3.3V from Pi)
- **V+** is servo power - connect to a separate 5-6V power supply capable of providing sufficient current for your servos
- The MG996R servo can draw up to 2.5A under load, so use a robust power supply

### I2C Address
- Default address: **0x40**
- Can be changed using address jumpers A0-A5 (up to 62 unique addresses)

### Wiring Diagram

```
Raspberry Pi 5               PCA9685
─────────────              ──────────
Pin 1 (3.3V) ─────────────→ VCC
Pin 3 (SDA)  ─────────────→ SDA
Pin 5 (SCL)  ─────────────→ SCL
Pin 6 (GND)  ─────────────→ GND
                            V+ ←── External 5-6V Power Supply
                            GND ←─┘
```

### MG996R Servo Connection

Connect the MG996R servo to any of the 16 output channels (0-15):

| Servo Wire | PCA9685 Output Pin |
|------------|-------------------|
| Brown (GND) | GND (row of pins) |
| Red (V+) | V+ (row of pins) |
| Orange (Signal) | PWM (row of pins) |

For head rotation, use **Channel 0** for simplicity.

### Software Setup
```bash
# Install required libraries
sudo pip3 install adafruit-circuitpython-pca9685 adafruit-circuitpython-servokit

# Enable I2C
sudo raspi-config
# Navigate to Interface Options → I2C → Enable
```

---

## 5️⃣ Cunyuer DC5 12V Dual Channel H Bridge Motor Driver

The H-Bridge motor driver controls the two DC gear motors for movement.

### Typical H-Bridge Pinout

| H-Bridge Pin | Function | Description |
|--------------|----------|-------------|
| VCC/+12V | Motor Power | 12V from battery |
| GND | Ground | Common ground |
| 5V (if available) | Logic Power | Some boards provide 5V output |
| IN1 | Motor A Control | Direction control |
| IN2 | Motor A Control | Direction control |
| IN3 | Motor B Control | Direction control |
| IN4 | Motor B Control | Direction control |
| ENA | Motor A Enable | PWM speed control (optional) |
| ENB | Motor B Enable | PWM speed control (optional) |
| OUT1, OUT2 | Motor A Output | Left motor connections |
| OUT3, OUT4 | Motor B Output | Right motor connections |

### Wiring to Raspberry Pi

| H-Bridge Pin | Raspberry Pi Pin | GPIO (BCM) | Purpose |
|--------------|-----------------|------------|---------|
| IN1 | Pin 29 | GPIO5 | Left motor forward |
| IN2 | Pin 31 | GPIO6 | Left motor reverse |
| IN3 | Pin 32 | GPIO12 | Right motor forward |
| IN4 | Pin 33 | GPIO13 | Right motor reverse |
| ENA | Pin 12 | GPIO18 | Left motor PWM speed* |
| ENB | Pin 35 | GPIO19 | Right motor PWM speed* |
| GND | Pin 6 or any GND | GND | Common ground |

> *Note: GPIO18 and GPIO19 are used by the WM8960 Audio HAT. If using both simultaneously, use software PWM on different pins (e.g., GPIO22, GPIO23) or control motors via the PCA9685.

### Alternative: Motor Control via PCA9685

If GPIO conflicts exist with the Audio HAT, use the PCA9685 to generate PWM for motor speed control:

| H-Bridge Pin | PCA9685 Channel |
|--------------|-----------------|
| ENA | Channel 14 |
| ENB | Channel 15 |

### Motor Connections

```
                    H-Bridge
                   ┌─────────┐
12V Battery (+) ───┤ +12V    │
12V Battery (-) ───┤ GND     │
                   │         │
Left Motor  (+) ───┤ OUT1    │
Left Motor  (-) ───┤ OUT2    │
                   │         │
Right Motor (+) ───┤ OUT3    │
Right Motor (-) ───┤ OUT4    │
                   └─────────┘
```

### Motor Direction Logic

| IN1 | IN2 | Motor A Action |
|-----|-----|----------------|
| LOW | LOW | Stop |
| HIGH | LOW | Forward |
| LOW | HIGH | Reverse |
| HIGH | HIGH | Brake |

Same logic applies to IN3/IN4 for Motor B.

---

## 6️⃣ Power Distribution System

### Power Requirements Summary

| Component | Voltage | Current (Max) |
|-----------|---------|---------------|
| Raspberry Pi 5 | 5V | 5A (25W recommended) |
| WM8960 Audio HAT | 5V (from Pi) | 500mA |
| 7" Display | 5V | 500mA |
| PCA9685 (logic) | 3.3V | 10mA |
| MG996R Servo | 5-6V | 2.5A (stall) |
| Geartesian Motors (x2) | 12V | 1-2A each |
| H-Bridge Logic | 5V | 50mA |

### Power Distribution Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    12V 5600mAh LiPo Battery                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   H-Bridge   │  │  5V 5A       │  │  6V 3A       │
    │   Motor      │  │  Voltage     │  │  Voltage     │
    │   Driver     │  │  Regulator   │  │  Regulator   │
    └──────────────┘  └──────────────┘  └──────────────┘
           │                │                │
           │                │                │
     ┌─────┴─────┐    ┌─────┴─────┐    ┌─────┴─────┐
     │           │    │           │    │           │
     ▼           ▼    ▼           │    ▼
┌─────────┐ ┌─────────┐ ┌─────────┐    ┌─────────┐
│  Left   │ │  Right  │ │Raspberry│    │ PCA9685 │
│  Motor  │ │  Motor  │ │  Pi 5   │    │Servo V+ │
│  12V    │ │  12V    │ │  5V/5A  │    │  6V/3A  │
└─────────┘ └─────────┘ └─────────┘    └─────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ WM8960   │  │ Display  │  │ PCA9685  │
        │ HAT      │  │ 5V USB   │  │ VCC 3.3V │
        │ (via Pi) │  │          │  │ (from Pi)│
        └──────────┘  └──────────┘  └──────────┘
```

### Wiring the Power System

1. **12V to Motors (via H-Bridge)**:
   - Connect 12V battery positive to H-Bridge VIN/+12V
   - Connect 12V battery negative to H-Bridge GND
   - Connect motors to H-Bridge outputs

2. **5V for Raspberry Pi and Electronics**:
   - Use a quality 5V 5A step-down converter (buck converter)
   - Input: 12V from battery
   - Output: 5V to Raspberry Pi USB-C power port
   - Also powers display via USB

3. **6V for Servos (optional separate regulator)**:
   - Use a 6V 3A step-down converter
   - Connect to PCA9685 V+ terminal
   - This provides clean servo power

4. **Common Ground**:
   - **CRITICAL**: All grounds must be connected together:
     - Battery GND
     - H-Bridge GND
     - Voltage regulator GND
     - Raspberry Pi GND
     - PCA9685 GND

---

## 7️⃣ Complete Wiring Diagram

```
                                    ┌─────────────────────────────────┐
                                    │      12V LiPo Battery           │
                                    │      5600mAh                    │
                                    └─────────┬───────────┬───────────┘
                                              │           │
                                              │           │
                              ┌───────────────┴───┐   ┌───┴───────────────┐
                              │    H-Bridge       │   │   5V/5A Buck      │
                              │    Motor Driver   │   │   Converter       │
                              │   ┌───────────┐   │   └─────────┬─────────┘
                              │   │  +12V GND │   │             │
                              │   └───────────┘   │             │
                              │   ┌───────────┐   │             │
                              │   │ IN1-IN4   │───┼─────────────┼──── GPIO5,6,12,13
                              │   │ ENA,ENB   │   │             │
                              │   └───────────┘   │             │
                              │   ┌───────────┐   │             │
                              │   │OUT1-2 3-4 │   │             │
                              │   └──┬────┬───┘   │             │
                              └──────│────│───────┘             │
                                     │    │                     │
                                ┌────┘    └────┐                │
                                ▼              ▼                │
                           ┌─────────┐    ┌─────────┐           │
                           │  LEFT   │    │  RIGHT  │           │
                           │  MOTOR  │    │  MOTOR  │           │
                           └─────────┘    └─────────┘           │
                                                                │
                                                                │
    ┌───────────────────────────────────────────────────────────┴───────┐
    │                                                                   │
    │                         RASPBERRY PI 5                            │
    │   ┌─────────────────────────────────────────────────────────┐     │
    │   │  USB-C ◄──────────────── 5V Power ──────────────────────│─────┤
    │   │                                                         │     │
    │   │  ┌──────────── 40-PIN GPIO HEADER ────────────────┐     │     │
    │   │  │                                                │     │     │
    │   │  │  Pin 1 (3.3V) ──────────────► PCA9685 VCC      │     │     │
    │   │  │  Pin 3 (SDA)  ──────────────► PCA9685 SDA      │     │     │
    │   │  │  Pin 5 (SCL)  ──────────────► PCA9685 SCL      │     │     │
    │   │  │  Pin 6 (GND)  ──────────────► Common GND       │     │     │
    │   │  │                                                │     │     │
    │   │  │  Pin 29 (GPIO5)  ───────────► H-Bridge IN1     │     │     │
    │   │  │  Pin 31 (GPIO6)  ───────────► H-Bridge IN2     │     │     │
    │   │  │  Pin 32 (GPIO12) ───────────► H-Bridge IN3     │     │     │
    │   │  │  Pin 33 (GPIO13) ───────────► H-Bridge IN4     │     │     │
    │   │  │                                                │     │     │
    │   │  │          WM8960 HAT (Mounted on top)           │     │     │
    │   │  │     Uses: GPIO2,3,17,18,19,20,21 + Power       │     │     │
    │   │  └────────────────────────────────────────────────┘     │     │
    │   │                                                         │     │
    │   │  CSI Port (CAM0) ◄─────── AI Camera Ribbon Cable        │     │
    │   │                                                         │     │
    │   │  Micro-HDMI ◄──────────── Display HDMI Cable            │     │
    │   │                                                         │     │
    │   │  USB Port ◄────────────── Display Touch USB             │     │
    │   └─────────────────────────────────────────────────────────┘     │
    │                                                                   │
    └───────────────────────────────────────────────────────────────────┘
                                      │
                                      │
    ┌─────────────────────────────────┴─────────────────────────────────┐
    │                           PCA9685                                 │
    │   ┌─────────────────────────────────────────────────────────┐     │
    │   │  VCC ◄─────────────────── 3.3V from Pi (Pin 1)          │     │
    │   │  SDA ◄─────────────────── GPIO2 (Pin 3)                 │     │
    │   │  SCL ◄─────────────────── GPIO3 (Pin 5)                 │     │
    │   │  GND ◄─────────────────── Ground (Pin 6)                │     │
    │   │  V+  ◄─────────────────── 6V from separate regulator    │     │
    │   │                                                         │     │
    │   │  Channel 0 ────────────► MG996R Servo (Head)            │     │
    │   │  Channels 1-15 ────────► Future expansion               │     │
    │   └─────────────────────────────────────────────────────────┘     │
    └───────────────────────────────────────────────────────────────────┘
```

---

## 8️⃣ GPIO Pin Allocation Summary

| GPIO (BCM) | Physical Pin | Used By | Function |
|------------|-------------|---------|----------|
| GPIO0 | 27 | ID EEPROM | Reserved (HAT ID) |
| GPIO1 | 28 | ID EEPROM | Reserved (HAT ID) |
| GPIO2 | 3 | WM8960 + PCA9685 | I2C SDA (shared) |
| GPIO3 | 5 | WM8960 + PCA9685 | I2C SCL (shared) |
| GPIO4 | 7 | Available | - |
| GPIO5 | 29 | H-Bridge | Motor A IN1 |
| GPIO6 | 31 | H-Bridge | Motor A IN2 |
| GPIO7 | 26 | Available | - |
| GPIO8 | 24 | Available | - |
| GPIO9 | 21 | Available | - |
| GPIO10 | 19 | Available | - |
| GPIO11 | 23 | Available | - |
| GPIO12 | 32 | H-Bridge | Motor B IN3 |
| GPIO13 | 33 | H-Bridge | Motor B IN4 |
| GPIO14 | 8 | Available | (UART TX) |
| GPIO15 | 10 | Available | (UART RX) |
| GPIO16 | 36 | Available | - |
| GPIO17 | 11 | WM8960 | Button (optional) |
| GPIO18 | 12 | WM8960 | I2S CLK |
| GPIO19 | 35 | WM8960 | I2S LRCLK |
| GPIO20 | 38 | WM8960 | I2S ADC |
| GPIO21 | 40 | WM8960 | I2S DAC |
| GPIO22 | 15 | Available | - |
| GPIO23 | 16 | Available | - |
| GPIO24 | 18 | Available | - |
| GPIO25 | 22 | Available | - |
| GPIO26 | 37 | Available | - |
| GPIO27 | 13 | Available | - |

---

## 9️⃣ Troubleshooting

### Common Issues

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| No audio output | Driver not installed | Run WM8960 install script |
| Motors not moving | Wrong GPIO pins | Verify IN1-IN4 connections |
| Servo jittering | Insufficient power | Use separate 6V power supply |
| Camera not detected | Ribbon cable loose | Reseat cable, check orientation |
| Display not working | Wrong HDMI port | Use HDMI0 (closest to USB-C) |
| I2C devices not found | I2C not enabled | Run `sudo raspi-config` |

### Testing Commands

```bash
# Check I2C devices (PCA9685 should show at 0x40)
sudo i2cdetect -y 1

# Test audio
speaker-test -c2

# Test camera
libcamera-hello

# Check GPIO
pinout  # Shows current GPIO state
```

---

## 🔧 Optional: Raspberry Pi Zero 2 W (Dedicated Motion Controller)

If using a Pi Zero 2 W as a dedicated motor controller:

### Communication Options

1. **UART** (recommended for low latency):
   - Pi 5 GPIO14 (TX) → Pi Zero GPIO15 (RX)
   - Pi 5 GPIO15 (RX) → Pi Zero GPIO14 (TX)
   - Common GND

2. **I2C** (Pi Zero as I2C slave):
   - Connect SDA to SDA, SCL to SCL
   - Common GND

3. **WiFi/Network** (easiest setup):
   - Both Pis on same network
   - WebSocket or REST API communication

### Pi Zero Wiring (Motion Controller)
- H-Bridge IN1-IN4 → Pi Zero GPIO pins
- PCA9685 → Pi Zero I2C
- Power from 5V regulator

---

## 📝 Assembly Order

1. **Test components individually first** before full assembly
2. Set up power distribution and verify voltages
3. Mount WM8960 Audio HAT on Pi 5
4. Connect display (HDMI + USB)
5. Connect AI Camera
6. Wire PCA9685 and test servo
7. Wire H-Bridge and test motors
8. Connect battery and verify full system

---

## 📚 References

- [Raspberry Pi 5 GPIO Pinout](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio-and-the-40-pin-header)
- [WM8960 Audio HAT Wiki](https://www.waveshare.com/wiki/WM8960_Audio_HAT)
- [PCA9685 Adafruit Guide](https://learn.adafruit.com/16-channel-pwm-servo-driver)
- [Raspberry Pi AI Camera Documentation](https://www.raspberrypi.com/documentation/accessories/ai-camera.html)

---

*Document created for the SysBot AI Voice Assistant on Wheels project.*
