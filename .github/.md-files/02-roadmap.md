<!--markdownlint-disable-->
# SysBot Development Roadmap

## Overview

This roadmap outlines the phased development approach for building the SysBot AI Voice Assistant on Wheels. The project is divided into three main parts with multiple milestones to ensure incremental progress and testable deliverables.

---

## Phase 1: Voice Assistant (Core AI Brain) 🧠

**Duration:** 4-6 weeks
**Goal:** Create a fully functional voice assistant on Raspberry Pi 5 with animated display

### Milestone 1.1: Environment Setup & Audio Pipeline
**Duration:** 1 week

- [ ] Set up Raspberry Pi 5 with Raspberry Pi OS (64-bit)
- [ ] Install Python 3.11+ development environment
- [ ] Configure WM8960 Audio HAT (integrated speakers & microphone)
- [ ] Install WM8960 driver and configure I2S audio
- [ ] Test audio input/output with PyAudio/sounddevice
- [ ] Install and configure ALSA/PulseAudio for audio routing
- [ ] Create audio utility module for recording and playback

**Deliverable:** Working audio capture and playback system

### Milestone 1.2: Wake Word Detection
**Duration:** 1 week

- [ ] Research and select wake word engine:
  - **Primary Choice:** OpenWakeWord (open-source, customizable)
  - **Alternative:** Porcupine (commercial, highly accurate)
- [ ] Implement always-on listening loop
- [ ] Train/configure custom wake word ("Hey SysBot")
- [ ] Add wake word detection callback system
- [ ] Implement LED/sound feedback on wake word detection

**Deliverable:** System responds to "Hey SysBot" wake word

### Milestone 1.3: Speech-to-Text (STT)
**Duration:** 1 week

- [ ] Implement STT pipeline:
  - **Local Option:** Whisper.cpp or Faster-Whisper (optimized for Pi 5)
  - **API Option:** OpenAI Whisper API, Google Speech-to-Text
- [ ] Create dropdown/config for switching between local/API modes
- [ ] Implement voice activity detection (VAD) for utterance endpoints
- [ ] Add audio buffering and streaming for real-time transcription
- [ ] Handle ambient noise and improve accuracy

**Deliverable:** Accurate speech transcription from microphone input

### Milestone 1.4: AI/LLM Integration
**Duration:** 1-2 weeks

- [ ] Set up LLM integration layer:
  - **Local Option:** Ollama with small models (phi3-mini, tinyllama)
  - **API Option:** OpenAI GPT-4, Claude, Google Gemini
- [ ] Create configuration system for model selection
- [ ] Implement conversation context management
- [ ] Add system prompts for personality (helpful cat robot)
- [ ] Create response streaming for faster perceived response time
- [ ] Implement function calling for future extensibility

**Deliverable:** Working AI conversation system

### Milestone 1.5: Text-to-Speech (TTS)
**Duration:** 1 week

- [ ] Implement TTS pipeline:
  - **Primary Choice:** Piper TTS (fast, local, high quality)
  - **Alternative:** Edge-TTS (online, free, high quality)
  - **Fallback:** eSpeak-ng (basic, offline)
- [ ] Select/create voice that matches cat robot personality
- [ ] Implement audio caching for common responses
- [ ] Add speech rate and pitch controls
- [ ] Integrate with audio output system

**Deliverable:** Natural-sounding spoken responses

### Milestone 1.6: Animated Display (Cat Robot UI)
**Duration:** 1-2 weeks

- [ ] Design cat robot character states:
  - 🐱 Idle (blinking, slight movement)
  - 👂 Listening (ears perked, attentive)
  - 🤔 Thinking (processing indicator)
  - 🗣️ Speaking (mouth movement, expressions)
  - 😺 Happy/Confirmation
  - 😿 Error/Confused
- [ ] Create frame-based animations (PNG sequences or sprites)
- [ ] Implement Pygame display system for animation rendering
- [ ] Build state machine for animation transitions
- [ ] Add lip-sync capability based on audio output
- [ ] Configure display for Raspberry Pi touchscreen or HDMI

**Deliverable:** Animated cat robot face with state-based expressions

### Milestone 1.7: Integration & Testing
**Duration:** 1 week

- [ ] Integrate all components into unified pipeline
- [ ] Create main application entry point
- [ ] Implement graceful error handling
- [ ] Add logging and debugging capabilities
- [ ] Test full conversation flow
- [ ] Optimize for latency and responsiveness
- [ ] Create configuration file system

**Deliverable:** Complete voice assistant with animated display

---

## Phase 2: Robot in Motion (Physical Mobility) 🤖

**Duration:** 4-5 weeks
**Goal:** Add physical movement capabilities with person-following

### Milestone 2.1: Hardware Setup & Motor Control
**Duration:** 1-2 weeks

- [ ] Acquire hardware:
  - 2x Geartesian DC 12V 100RPM gear motors
  - Cunyuer DC5 12V Dual Channel H Bridge motor driver
  - MG996R servo motor (high-torque for head rotation)
  - PCA9685 I2C PWM driver (optional, for precise servo control)
  - Power supply/battery system (12V for motors, 5V for Pi)
  - Chassis/frame for robot body
- [ ] Wire Cunyuer H Bridge motor driver to Raspberry Pi GPIO
- [ ] Configure PCA9685 I2C servo driver (if using)
- [ ] Install GPIO libraries (gpiozero, RPi.GPIO, or pigpio)
- [ ] Install Adafruit PCA9685 library for I2C servo control
- [ ] Implement basic motor control (forward, backward, turn)
- [ ] Calibrate Geartesian motor speeds for straight movement
- [ ] Implement MG996R servo control for head panning

**Deliverable:** Basic motor control from Python

### Milestone 2.2: Camera Integration
**Duration:** 1 week

- [ ] Set up Raspberry Pi AI Camera (with built-in AI accelerator)
- [ ] Configure camera interface (libcamera/picamera2)
- [ ] Implement video streaming pipeline
- [ ] Add frame capture for processing
- [ ] Test camera mounting on servo for head tracking

**Deliverable:** Working camera feed accessible from Python

### Milestone 2.3: Person Detection & Tracking
**Duration:** 1-2 weeks

- [ ] Implement person detection:
  - **Option 1:** OpenCV with MobileNet-SSD
  - **Option 2:** MediaPipe Pose/Holistic
  - **Option 3:** TensorFlow Lite with PoseNet
- [ ] Create person bounding box detection
- [ ] Implement person tracking across frames
- [ ] Calculate person position relative to robot
- [ ] Add depth estimation (if using stereo or ToF sensor)
- [ ] Handle multiple people (focus on primary target)

**Deliverable:** Real-time person detection and position tracking

### Milestone 2.4: Follow-Me Algorithm
**Duration:** 1 week

- [ ] Design follow behavior logic:
  - Maintain optimal following distance
  - Center person in camera view
  - Smooth movement to avoid jerky motion
- [ ] Implement PID controller for smooth following
- [ ] Add obstacle awareness (basic collision avoidance)
- [ ] Create head tracking (servo follows person)
- [ ] Implement "lost target" behavior (search pattern)
- [ ] Add voice commands for follow mode control

**Deliverable:** Robot follows person around the room

### Milestone 2.5: Multi-Controller Architecture (Optional)
**Duration:** 1 week (if using Pi Zero 2)

- [ ] Decide on architecture:
  - **Option A:** Single Pi 5 handles everything
  - **Option B:** Pi 5 (brain) + Pi Zero 2 (motion)
- [ ] If Option B:
  - Set up communication (UART, I2C, or WiFi)
  - Create command protocol
  - Implement motor control on Pi Zero 2
  - Sync sensor data between controllers

**Deliverable:** Stable multi-controller communication (if applicable)

### Milestone 2.6: Motion Safety & Integration
**Duration:** 1 week

- [ ] Add safety features:
  - Emergency stop capability
  - Speed limits
  - Collision detection (ultrasonic/IR sensors)
  - Low battery protection
- [ ] Integrate motion with voice assistant
- [ ] Voice commands for movement control
- [ ] Status feedback through UI animations
- [ ] Test complete system integration

**Deliverable:** Safe, integrated voice assistant robot

---

## Phase 3: Manual Control (Mobile App) 📱

**Duration:** 3-4 weeks
**Goal:** Create mobile app for remote robot control

### Milestone 3.1: Robot API Server
**Duration:** 1 week

- [ ] Create REST/WebSocket API on robot:
  - **Framework:** Flask with Flask-SocketIO or FastAPI
  - Movement commands (forward, back, left, right, stop)
  - Head servo control
  - Mode switching (auto-follow vs manual)
  - Status endpoints (battery, connection, mode)
- [ ] Implement WebSocket for real-time control
- [ ] Add video streaming endpoint (MJPEG or WebRTC)
- [ ] Create authentication system
- [ ] Handle concurrent connections

**Deliverable:** Robot API accessible over local network

### Milestone 3.2: Mobile App Development
**Duration:** 2-3 weeks

- [ ] Select framework:
  - **Primary:** Flutter (cross-platform, good performance)
  - **Alternative:** React Native
  - **Simple:** Progressive Web App (PWA)
- [ ] Design UI:
  - Virtual joystick for movement
  - Head control slider/pad
  - Live camera feed display
  - Mode toggle (Auto/Manual)
  - Connection status
  - Battery indicator
- [ ] Implement WebSocket connection
- [ ] Create joystick control component
- [ ] Add video feed viewer
- [ ] Implement haptic feedback
- [ ] Test on iOS and Android

**Deliverable:** Working mobile control app

### Milestone 3.3: Advanced Features
**Duration:** 1 week

- [ ] Add voice chat through app (speak to robot remotely)
- [ ] Implement recording/playback of paths
- [ ] Add gesture controls
- [ ] Create home base/docking behavior
- [ ] Implement scheduled follow times
- [ ] Add "come to me" voice command

**Deliverable:** Feature-complete control system

---

## Future Enhancements 🚀

These features can be added after the core system is complete:

### Vision Enhancements
- [ ] Face recognition for family members
- [ ] Object detection and identification
- [ ] Room mapping and navigation
- [ ] Gesture recognition for commands

### AI Enhancements
- [ ] Long-term memory and context
- [ ] Personalized responses per user
- [ ] Smart home integration (Home Assistant)
- [ ] Calendar and reminder integration
- [ ] News and weather briefings

### Physical Enhancements
- [ ] Arm/gripper for object manipulation
- [ ] Additional sensors (temperature, air quality)
- [ ] Better autonomous navigation (SLAM)
- [ ] Wireless charging dock

### Social Features
- [ ] Multi-robot communication
- [ ] Pet-like behaviors and personality
- [ ] Learning from interactions
- [ ] Emotional state system

---

## Development Dependencies Summary

### Software Requirements

| Component | Primary Choice | Alternative |
|-----------|---------------|-------------|
| OS | Raspberry Pi OS 64-bit | Ubuntu Server |
| Language | Python 3.11+ | - |
| Wake Word | OpenWakeWord | Porcupine |
| STT | Faster-Whisper | Whisper API |
| LLM | Ollama + phi3 | OpenAI GPT |
| TTS | Piper TTS | Edge-TTS |
| Display | Pygame | Tkinter |
| Motor Control | gpiozero | RPi.GPIO |
| Vision | OpenCV + MediaPipe | TensorFlow Lite |
| API Server | Flask-SocketIO | FastAPI |
| Mobile App | Flutter | React Native |

### Hardware Requirements

| Component | Specification |
|-----------|--------------|
| Main Controller | Raspberry Pi 5 (8GB recommended) |
| Optional Controller | Raspberry Pi Zero 2 W (for dedicated motion control) |
| Display | Hoysond 7" Touchscreen (1024x600) |
| Camera | Raspberry Pi AI Camera (built-in AI accelerator) |
| Audio HAT | WM8960 Audio HAT (integrated speakers & microphone) |
| Motors | 2x Geartesian DC 12V 100RPM gear motors |
| Motor Driver | Cunyuer DC5 12V Dual Channel H Bridge |
| Servo | MG996R (high-torque for head rotation) |
| Servo Driver | PCA9685 I2C PWM Driver (optional, for precise servo control) |
| Power | LiPo battery pack + voltage regulators |
| Chassis | Custom or kit-based robot platform |

---

## Timeline Summary

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| Phase 1 | 4-6 weeks | Voice assistant with animated UI |
| Phase 2 | 4-5 weeks | Mobile robot with follow-me |
| Phase 3 | 3-4 weeks | Mobile app control |
| **Total** | **11-15 weeks** | **Complete SysBot** |

---

## Getting Started

To begin development:

1. Start with [03-architecture.md](03-architecture.md) for system design
2. Set up the Raspberry Pi 5 development environment
3. Follow milestones in order within each phase
4. Test each milestone before proceeding
5. Document issues and solutions as you go

Good luck building SysBot! 🐱🤖
