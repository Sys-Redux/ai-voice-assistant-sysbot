<!--markdownlint-disable-->
# SysBot System Architecture

## Overview

This document describes the proposed software and hardware architecture for SysBot, an AI-powered voice assistant robot. The system is designed to be modular, allowing for independent development and testing of each component.

## APP

*Main Screen*

The main screen will be the AI voice assistant, which is a cat-robot with different animations for different "moods" (listening, thinking, speaking, idle). This animation will be in the center of the screen with a studio black background.
    
The app will always be listening for the user to say it's wake word. Once user says wake word, the speech-to-text will be triggered, then an API request will be sent, then the response will be spoken.
    
The screen that the app is displayed is the head of a robot. The body of the robot is an RC car. The app is running on a raspberry pi 5 & we will be using an AI camera to detect user's face so that the robot can follow the user around in the phone sical world.
*Web App Side-App*
    
There will be an app that will connect to the robot(the app running on the robot), intended to be accessed on mobile, that will allow user to have more control over the robot.
    
**Settings-Button**
        
AI-Select
            
This button will present a drop-down menu in which the user can choose which AI model will be supplying answers via the models API.
        
Voice-Select
            
Dropdown to select which voice the assistant will use. Each option of the drop-down will have a button to hear a sample of that voice.
    
Manual-Control-Button
        
Clicking this button will bring up a joystick, granting the user manual control over the rc-car. (The default control of the rc car is AI using facial recognition to follow the user around).

**Architectural Considerations**
    
Calling an API to get an answer is great, but we need to implement systems that will make this robot/app learn the user over time. First thing that comes to mind is a RAG system so that the app will learn from every request/response. We're aiming for something similar to chatGPT, as chatGPT adapts to the user over time and has memory of previous conversations.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SYSBOT SYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     MOBILE APP (Flutter/PWA)                         │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│  │  │  Joystick   │ │ Video Feed  │ │ Status View │ │ Voice Chat  │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │   │
│  └───────────────────────────────┬─────────────────────────────────────┘   │
│                                  │ WebSocket/HTTP                           │
│  ┌───────────────────────────────┴─────────────────────────────────────┐   │
│  │                      RASPBERRY PI 5 (Main Brain)                     │   │
│  │                                                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    VOICE ASSISTANT MODULE                     │    │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │    │   │
│  │  │  │  Wake   │→│  STT   │→│   LLM   │→│  TTS   │→│ Audio  │ │    │   │
│  │  │  │  Word   │ │(Whisper)│ │(Ollama) │ │(Piper) │ │ Output │ │    │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └────────┘ │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    DISPLAY MODULE (Pygame)                    │    │   │
│  │  │  ┌─────────────────────────────────────────────────────────┐ │    │   │
│  │  │  │     🐱 Animated Cat Robot Face (State-based)             │ │    │   │
│  │  │  │     States: Idle | Listening | Thinking | Speaking       │ │    │   │
│  │  │  └─────────────────────────────────────────────────────────┘ │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    VISION MODULE (OpenCV)                     │    │   │
│  │  │  ┌─────────┐ ┌─────────────┐ ┌──────────────┐               │    │   │
│  │  │  │ Camera  │→│   Person    │→│   Tracking   │               │    │   │
│  │  │  │ Capture │ │  Detection  │ │  Algorithm   │               │    │   │
│  │  │  └─────────┘ └─────────────┘ └──────────────┘               │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    MOTION MODULE (gpiozero)                   │    │   │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│    │   │
│  │  │  │ Motor       │ │ Servo       │ │ Follow-Me               ││    │   │
│  │  │  │ Controller  │ │ Controller  │ │ Controller              ││    │   │
│  │  │  └─────────────┘ └─────────────┘ └─────────────────────────┘│    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  │                                                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │                    API SERVER (Flask-SocketIO)                │    │   │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────────┐│    │   │
│  │  │  │  REST   │ │WebSocket│ │  Video  │ │  Command Handler    ││    │   │
│  │  │  │ Routes  │ │ Events  │ │ Stream  │ │                     ││    │   │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────────────────┘│    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
sysbot/
├── .github/
│   ├── copilot-instructions.md
│   └── .md-files/
│       ├── 01-project-vision.md
│       ├── 02-roadmap.md
│       └── 03-architecture.md
│
├── md-files/
│   ├── 02-roadmap.md
│   └── 03-architecture.md
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Application entry point
│   ├── config.py                  # Configuration management
│   │
│   ├── voice/                     # Voice Assistant Module
│   │   ├── __init__.py
│   │   ├── audio_manager.py       # Audio input/output handling
│   │   ├── wake_word.py           # Wake word detection
│   │   ├── stt.py                 # Speech-to-text
│   │   ├── llm.py                 # LLM integration (Ollama/API)
│   │   ├── tts.py                 # Text-to-speech
│   │   └── conversation.py        # Conversation management
│   │
│   ├── display/                   # Display Module
│   │   ├── __init__.py
│   │   ├── renderer.py            # Pygame display renderer
│   │   ├── animation.py           # Animation state machine
│   │   ├── sprites.py             # Sprite management
│   │   └── states/                # Animation states
│   │       ├── idle.py
│   │       ├── listening.py
│   │       ├── thinking.py
│   │       └── speaking.py
│   │
│   ├── vision/                    # Vision Module
│   │   ├── __init__.py
│   │   ├── camera.py              # Camera capture
│   │   ├── detector.py            # Person detection
│   │   └── tracker.py             # Object tracking
│   │
│   ├── motion/                    # Motion Module
│   │   ├── __init__.py
│   │   ├── motor_controller.py    # DC motor control
│   │   ├── servo_controller.py    # Servo motor control
│   │   ├── follow_me.py           # Follow-me algorithm
│   │   └── safety.py              # Safety systems
│   │
│   ├── api/                       # API Server Module
│   │   ├── __init__.py
│   │   ├── server.py              # Flask app setup
│   │   ├── routes.py              # REST endpoints
│   │   ├── websocket.py           # WebSocket handlers
│   │   └── auth.py                # Authentication
│   │
│   └── utils/                     # Utilities
│       ├── __init__.py
│       ├── logger.py              # Logging utilities
│       ├── events.py              # Event bus system
│       └── gpio_utils.py          # GPIO helpers
│
├── assets/
│   ├── sprites/                   # Cat robot animation frames
│   │   ├── idle/
│   │   ├── listening/
│   │   ├── thinking/
│   │   └── speaking/
│   ├── sounds/                    # Sound effects
│   │   ├── wake.wav
│   │   ├── confirm.wav
│   │   └── error.wav
│   └── voices/                    # TTS voice models
│
├── config/
│   ├── default.yaml               # Default configuration
│   └── production.yaml            # Production overrides
│
├── tests/
│   ├── test_voice/
│   ├── test_display/
│   ├── test_vision/
│   └── test_motion/
│
├── mobile_app/                    # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── services/
│   ├── pubspec.yaml
│   └── README.md
│
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
└── README.md                      # Project documentation
```

---

## Module Details

### 1. Voice Assistant Module

The voice assistant is the core brain of SysBot, handling all speech interaction.

#### 1.1 Audio Pipeline

**Hardware:** WM8960 Audio HAT (I2S interface with integrated speakers & microphone)

```
┌──────────────────┐     ┌─────────────┐     ┌────────────┐
│ WM8960 Audio HAT │────→│   PyAudio   │────→│   Buffer   │
│   (Microphone)   │     │   Capture   │     │   (Ring)   │
└──────────────────┘     └─────────────┘     └─────┬──────┘
                                                    │
                                                    ▼
┌──────────────────┐     ┌─────────────┐     ┌────────────┐
│ WM8960 Audio HAT │←────│   PyAudio   │←────│   Queue    │
│    (Speakers)    │     │   Playback  │     │  (Audio)   │
└──────────────────┘     └─────────────┘     └────────────┘
```

**Key Classes:**

```python
# src/voice/audio_manager.py

class AudioManager:
    """Manages audio input and output streams."""

    def __init__(self, config: AudioConfig):
        self.sample_rate = config.sample_rate  # 16000 Hz
        self.chunk_size = config.chunk_size    # 1024 samples
        self.input_device = config.input_device
        self.output_device = config.output_device

    async def start_recording(self) -> AsyncIterator[bytes]:
        """Yields audio chunks from microphone."""
        pass

    async def play_audio(self, audio_data: bytes) -> None:
        """Plays audio through speakers."""
        pass

    def get_audio_level(self) -> float:
        """Returns current audio input level (0.0-1.0)."""
        pass
```

#### 1.2 Wake Word Detection

```python
# src/voice/wake_word.py

class WakeWordDetector:
    """Detects wake word using OpenWakeWord."""

    def __init__(self, wake_word: str = "hey_sysbot"):
        self.model = openwakeword.Model(wake_word)
        self.threshold = 0.5
        self.on_wake = Event()  # Triggered on wake word

    async def listen(self, audio_stream: AsyncIterator[bytes]) -> None:
        """Continuously listens for wake word."""
        async for chunk in audio_stream:
            prediction = self.model.predict(chunk)
            if prediction > self.threshold:
                await self.on_wake.trigger()
```

#### 1.3 Speech-to-Text

```python
# src/voice/stt.py

class STTEngine(ABC):
    """Abstract base for STT engines."""

    @abstractmethod
    async def transcribe(self, audio: bytes) -> str:
        """Transcribe audio to text."""
        pass

class WhisperLocalSTT(STTEngine):
    """Local Whisper using faster-whisper."""

    def __init__(self, model_size: str = "base"):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    async def transcribe(self, audio: bytes) -> str:
        segments, info = self.model.transcribe(audio)
        return " ".join([s.text for s in segments])

class WhisperAPISTT(STTEngine):
    """OpenAI Whisper API."""

    async def transcribe(self, audio: bytes) -> str:
        # Use OpenAI API
        pass
```

#### 1.4 LLM Integration

```python
# src/voice/llm.py

class LLMEngine(ABC):
    """Abstract base for LLM engines."""

    @abstractmethod
    async def chat(self, messages: List[Message]) -> AsyncIterator[str]:
        """Stream chat response."""
        pass

class OllamaLLM(LLMEngine):
    """Local LLM using Ollama."""

    def __init__(self, model: str = "phi3:mini"):
        self.model = model
        self.base_url = "http://localhost:11434"
        self.system_prompt = """You are SysBot, a helpful and friendly cat robot
        assistant. You have a playful personality and like to make cat puns
        occasionally. Keep responses concise for voice interaction."""

    async def chat(self, messages: List[Message]) -> AsyncIterator[str]:
        from ollama import AsyncClient
        client = AsyncClient()

        full_messages = [
            {"role": "system", "content": self.system_prompt},
            *[{"role": m.role, "content": m.content} for m in messages]
        ]

        async for chunk in await client.chat(
            model=self.model,
            messages=full_messages,
            stream=True
        ):
            yield chunk['message']['content']

class OpenAILLM(LLMEngine):
    """OpenAI GPT API."""
    pass
```

#### 1.5 Text-to-Speech

```python
# src/voice/tts.py

class TTSEngine(ABC):
    """Abstract base for TTS engines."""

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """Convert text to audio bytes."""
        pass

class PiperTTS(TTSEngine):
    """Local TTS using Piper."""

    def __init__(self, voice: str = "en_US-lessac-medium"):
        import piper
        self.voice = piper.Voice(voice)

    async def synthesize(self, text: str) -> bytes:
        audio = self.voice.synthesize(text)
        return audio.raw_bytes

class EdgeTTS(TTSEngine):
    """Online TTS using Microsoft Edge."""

    async def synthesize(self, text: str) -> bytes:
        import edge_tts
        communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        return audio_data
```

---

### 2. Display Module

The display module renders the animated cat robot face using Pygame.

#### 2.1 State Machine

```
          ┌─────────────────────────────────────────────────┐
          │                                                 │
          ▼                                                 │
     ┌─────────┐    wake word    ┌───────────┐             │
     │  IDLE   │────────────────→│ LISTENING │             │
     └─────────┘                 └─────┬─────┘             │
          ▲                            │                    │
          │                        speech ends             │
          │                            │                    │
          │                            ▼                    │
          │                      ┌───────────┐             │
          │                      │ THINKING  │             │
          │                      └─────┬─────┘             │
          │                            │                    │
          │                       response ready            │
          │                            │                    │
          │                            ▼                    │
          │                      ┌───────────┐             │
          └──────────────────────│ SPEAKING  │─────────────┘
               speech ends       └───────────┘
```

#### 2.2 Animation System

```python
# src/display/animation.py

class AnimationState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    HAPPY = "happy"
    ERROR = "error"

class Animation:
    """Handles frame-based sprite animation."""

    def __init__(self, frames: List[pygame.Surface], fps: int = 12):
        self.frames = frames
        self.fps = fps
        self.current_frame = 0
        self.last_update = 0

    def update(self, dt: float) -> pygame.Surface:
        """Update animation and return current frame."""
        self.last_update += dt
        if self.last_update >= 1.0 / self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = 0
        return self.frames[self.current_frame]

class AnimationController:
    """Controls animation state transitions."""

    def __init__(self):
        self.animations: Dict[AnimationState, Animation] = {}
        self.current_state = AnimationState.IDLE
        self.transition_queue = []

    def load_animations(self, assets_path: str):
        """Load all animation frames from assets."""
        for state in AnimationState:
            frames = self._load_frames(f"{assets_path}/{state.value}")
            self.animations[state] = Animation(frames)

    def set_state(self, state: AnimationState):
        """Transition to new animation state."""
        self.current_state = state

    def get_current_frame(self, dt: float) -> pygame.Surface:
        """Get current animation frame."""
        return self.animations[self.current_state].update(dt)
```

#### 2.3 Display Renderer

```python
# src/display/renderer.py

class DisplayRenderer:
    """Main Pygame display renderer."""

    def __init__(self, width: int = 800, height: int = 480):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("SysBot")
        self.clock = pygame.time.Clock()
        self.animation_controller = AnimationController()
        self.running = True

    async def run(self):
        """Main display loop."""
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Draw current animation frame
            frame = self.animation_controller.get_current_frame(dt)
            self.screen.blit(frame, self._center_position(frame))

            pygame.display.flip()
            await asyncio.sleep(0)  # Yield to event loop

    def _center_position(self, surface: pygame.Surface) -> Tuple[int, int]:
        """Calculate centered position for surface."""
        x = (self.screen.get_width() - surface.get_width()) // 2
        y = (self.screen.get_height() - surface.get_height()) // 2
        return (x, y)
```

---

### 3. Vision Module

The vision module handles camera input and person detection for follow-me functionality.

#### 3.1 Person Detection Pipeline

```
┌────────────┐     ┌──────────────┐     ┌────────────────┐
│   Camera   │────→│   OpenCV     │────→│   MediaPipe    │
│  (Pi Cam)  │     │   Capture    │     │   Detection    │
└────────────┘     └──────────────┘     └───────┬────────┘
                                                 │
                                                 ▼
                   ┌──────────────┐     ┌────────────────┐
                   │   Tracking   │←────│   Bounding     │
                   │   Algorithm  │     │     Box        │
                   └──────┬───────┘     └────────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │   Position   │
                   │   Relative   │
                   │   to Robot   │
                   └──────────────┘
```

#### 3.2 Implementation

```python
# src/vision/detector.py

class PersonDetector:
    """Detects and tracks people using MediaPipe."""

    def __init__(self):
        import mediapipe as mp
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, frame: np.ndarray) -> Optional[PersonDetection]:
        """Detect person in frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:
            # Calculate bounding box from landmarks
            landmarks = results.pose_landmarks.landmark
            x_coords = [l.x for l in landmarks]
            y_coords = [l.y for l in landmarks]

            return PersonDetection(
                bbox=BoundingBox(
                    x=min(x_coords),
                    y=min(y_coords),
                    width=max(x_coords) - min(x_coords),
                    height=max(y_coords) - min(y_coords)
                ),
                center=Point(
                    x=sum(x_coords) / len(x_coords),
                    y=sum(y_coords) / len(y_coords)
                ),
                confidence=0.9
            )
        return None
```

```python
# src/vision/tracker.py

class PersonTracker:
    """Tracks person position over time."""

    def __init__(self):
        self.last_position: Optional[Point] = None
        self.velocity = Point(0, 0)
        self.smoothing = 0.3

    def update(self, detection: Optional[PersonDetection]) -> TrackingResult:
        """Update tracking with new detection."""
        if detection is None:
            return TrackingResult(
                found=False,
                position=self.last_position,
                velocity=self.velocity
            )

        # Smooth position update
        if self.last_position:
            new_pos = Point(
                x=self.smoothing * detection.center.x +
                   (1 - self.smoothing) * self.last_position.x,
                y=self.smoothing * detection.center.y +
                   (1 - self.smoothing) * self.last_position.y
            )
            self.velocity = Point(
                x=new_pos.x - self.last_position.x,
                y=new_pos.y - self.last_position.y
            )
        else:
            new_pos = detection.center

        self.last_position = new_pos

        return TrackingResult(
            found=True,
            position=new_pos,
            velocity=self.velocity
        )
```

---

### 4. Motion Module

The motion module controls the robot's physical movement.

#### 4.1 Hardware Interface

```
                    ┌──────────────────┐
                    │   Raspberry Pi   │
                    │    GPIO / I2C    │
                    └────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    ┌──────────┐      ┌──────────┐       ┌──────────┐
    │ Cunyuer  │      │ Cunyuer  │       │ PCA9685  │
    │ H-Bridge │      │ H-Bridge │       │ I2C PWM  │
    │ (Motor L)│      │ (Motor R)│       │ Driver   │
    └────┬─────┘      └────┬─────┘       └────┬─────┘
         │                 │                  │
         ▼                 ▼                  ▼
    ┌──────────┐      ┌──────────┐       ┌──────────┐
    │Geartesian│      │Geartesian│       │  MG996R  │
    │ DC 12V   │      │ DC 12V   │       │  Servo   │
    │ 100RPM   │      │ 100RPM   │       │  (Head)  │
    └──────────┘      └──────────┘       └──────────┘
```

#### 4.2 Motor Control

```python
# src/motion/motor_controller.py

from gpiozero import Motor, PWMOutputDevice

class MotorController:
    """Controls DC motors for robot movement."""

    def __init__(self, config: MotorConfig):
        # Left motor
        self.left_motor = Motor(
            forward=config.left_forward_pin,  # GPIO17
            backward=config.left_backward_pin  # GPIO27
        )
        self.left_pwm = PWMOutputDevice(config.left_enable_pin)  # GPIO22

        # Right motor
        self.right_motor = Motor(
            forward=config.right_forward_pin,  # GPIO23
            backward=config.right_backward_pin  # GPIO24
        )
        self.right_pwm = PWMOutputDevice(config.right_enable_pin)  # GPIO25

        self.max_speed = 1.0

    def move(self, left_speed: float, right_speed: float):
        """Set motor speeds (-1.0 to 1.0)."""
        # Clamp speeds
        left_speed = max(-self.max_speed, min(self.max_speed, left_speed))
        right_speed = max(-self.max_speed, min(self.max_speed, right_speed))

        # Left motor
        if left_speed >= 0:
            self.left_motor.forward()
        else:
            self.left_motor.backward()
        self.left_pwm.value = abs(left_speed)

        # Right motor
        if right_speed >= 0:
            self.right_motor.forward()
        else:
            self.right_motor.backward()
        self.right_pwm.value = abs(right_speed)

    def forward(self, speed: float = 0.5):
        """Move forward."""
        self.move(speed, speed)

    def backward(self, speed: float = 0.5):
        """Move backward."""
        self.move(-speed, -speed)

    def turn_left(self, speed: float = 0.5):
        """Turn left in place."""
        self.move(-speed, speed)

    def turn_right(self, speed: float = 0.5):
        """Turn right in place."""
        self.move(speed, -speed)

    def stop(self):
        """Stop all motors."""
        self.left_motor.stop()
        self.right_motor.stop()
        self.left_pwm.value = 0
        self.right_pwm.value = 0
```

```python
# src/motion/servo_controller.py

from gpiozero import AngularServo

class ServoController:
    """Controls servo motor for head rotation."""

    def __init__(self, pin: int = 18):
        self.servo = AngularServo(
            pin,
            min_angle=-90,
            max_angle=90,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )
        self.current_angle = 0

    def set_angle(self, angle: float):
        """Set servo to specific angle (-90 to 90)."""
        angle = max(-90, min(90, angle))
        self.servo.angle = angle
        self.current_angle = angle

    def pan_to(self, target_angle: float, speed: float = 2.0):
        """Smoothly pan to target angle."""
        step = speed if target_angle > self.current_angle else -speed
        while abs(self.current_angle - target_angle) > abs(step):
            self.current_angle += step
            self.servo.angle = self.current_angle
            time.sleep(0.02)
        self.set_angle(target_angle)

    def center(self):
        """Center the servo."""
        self.set_angle(0)
```

#### 4.3 Follow-Me Controller

```python
# src/motion/follow_me.py

class FollowMeController:
    """Controls robot to follow detected person."""

    def __init__(self, motor: MotorController, servo: ServoController):
        self.motor = motor
        self.servo = servo

        # PID controllers
        self.turn_pid = PIDController(kp=0.5, ki=0.01, kd=0.1)
        self.speed_pid = PIDController(kp=0.3, ki=0.01, kd=0.05)

        # Target parameters
        self.target_distance = 1.5  # meters
        self.center_x = 0.5  # normalized (0-1)

        self.enabled = False

    def update(self, tracking: TrackingResult):
        """Update movement based on tracking result."""
        if not self.enabled or not tracking.found:
            self.motor.stop()
            return

        # Calculate error from center
        x_error = tracking.position.x - self.center_x

        # Calculate turn speed (proportional to horizontal offset)
        turn_speed = self.turn_pid.update(x_error)

        # Calculate forward speed (based on estimated distance)
        # Larger bounding box = closer = slower
        distance_error = self.target_distance - self._estimate_distance(tracking)
        forward_speed = self.speed_pid.update(distance_error)

        # Apply to motors (differential drive)
        left_speed = forward_speed - turn_speed
        right_speed = forward_speed + turn_speed

        self.motor.move(left_speed, right_speed)

        # Pan head servo to track person
        head_angle = -x_error * 90  # Map to servo angle
        self.servo.set_angle(head_angle)

    def _estimate_distance(self, tracking: TrackingResult) -> float:
        """Estimate distance based on detection size."""
        # Rough estimation: larger detection = closer
        # This should be calibrated for your camera
        if tracking.bbox:
            return 1.0 / (tracking.bbox.height + 0.1)
        return self.target_distance

    def enable(self):
        """Enable follow mode."""
        self.enabled = True

    def disable(self):
        """Disable follow mode and stop."""
        self.enabled = False
        self.motor.stop()
```

---

### 5. API Server Module

The API server enables remote control from the mobile app.

#### 5.1 Server Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask-SocketIO Server                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  REST API                    WebSocket Events                │
│  ─────────                   ────────────────                │
│  GET  /api/status            connect                         │
│  GET  /api/battery           disconnect                      │
│  POST /api/mode              move (joystick data)            │
│  GET  /api/stream            servo (angle)                   │
│                              voice (audio chunks)            │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Video Streaming: MJPEG over HTTP (/api/stream)             │
│                   or WebRTC for lower latency                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 5.2 Implementation

```python
# src/api/server.py

from flask import Flask, jsonify, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Robot components (injected)
motor_controller = None
servo_controller = None
follow_controller = None
camera = None

@app.route('/api/status')
def get_status():
    """Get robot status."""
    return jsonify({
        'mode': 'follow' if follow_controller.enabled else 'manual',
        'battery': get_battery_level(),
        'connected': True
    })

@app.route('/api/mode', methods=['POST'])
def set_mode():
    """Set robot mode (follow/manual)."""
    data = request.json
    mode = data.get('mode', 'manual')

    if mode == 'follow':
        follow_controller.enable()
    else:
        follow_controller.disable()

    return jsonify({'mode': mode})

@app.route('/api/stream')
def video_stream():
    """MJPEG video stream."""
    def generate():
        while True:
            frame = camera.get_frame()
            if frame is not None:
                _, jpeg = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       jpeg.tobytes() + b'\r\n')

    return Response(
        generate(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('status', {'connected': True})

@socketio.on('move')
def handle_move(data):
    """Handle movement commands from joystick."""
    if follow_controller.enabled:
        return  # Ignore in follow mode

    x = data.get('x', 0)  # -1 to 1 (left/right)
    y = data.get('y', 0)  # -1 to 1 (backward/forward)

    # Convert joystick to differential drive
    left_speed = y + x
    right_speed = y - x

    motor_controller.move(left_speed, right_speed)

@socketio.on('servo')
def handle_servo(data):
    """Handle head servo control."""
    angle = data.get('angle', 0)
    servo_controller.set_angle(angle)

@socketio.on('stop')
def handle_stop():
    """Emergency stop."""
    motor_controller.stop()

def run_server():
    """Run the Flask-SocketIO server."""
    socketio.run(app, host='0.0.0.0', port=5000)
```

---

### 6. Event System

The event system enables communication between modules.

```python
# src/utils/events.py

from typing import Callable, Dict, List
from enum import Enum, auto

class Event(Enum):
    WAKE_WORD_DETECTED = auto()
    SPEECH_START = auto()
    SPEECH_END = auto()
    TRANSCRIPTION_COMPLETE = auto()
    LLM_RESPONSE_START = auto()
    LLM_RESPONSE_CHUNK = auto()
    LLM_RESPONSE_END = auto()
    TTS_START = auto()
    TTS_END = auto()
    PERSON_DETECTED = auto()
    PERSON_LOST = auto()
    MODE_CHANGED = auto()
    ERROR = auto()

class EventBus:
    """Central event bus for inter-module communication."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.listeners: Dict[Event, List[Callable]] = {}
        return cls._instance

    def subscribe(self, event: Event, callback: Callable):
        """Subscribe to an event."""
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)

    def unsubscribe(self, event: Event, callback: Callable):
        """Unsubscribe from an event."""
        if event in self.listeners:
            self.listeners[event].remove(callback)

    async def emit(self, event: Event, data: any = None):
        """Emit an event to all listeners."""
        if event in self.listeners:
            for callback in self.listeners[event]:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
```

---

### 7. Configuration System

```python
# src/config.py

from dataclasses import dataclass
from typing import Literal
import yaml

@dataclass
class AudioConfig:
    sample_rate: int = 16000
    chunk_size: int = 1024
    input_device: str = "default"
    output_device: str = "default"

@dataclass
class VoiceConfig:
    wake_word: str = "hey_sysbot"
    stt_engine: Literal["local", "api"] = "local"
    stt_model: str = "base"
    llm_engine: Literal["ollama", "openai"] = "ollama"
    llm_model: str = "phi3:mini"
    tts_engine: Literal["piper", "edge"] = "piper"
    tts_voice: str = "en_US-lessac-medium"

@dataclass
class MotorConfig:
    left_forward_pin: int = 17
    left_backward_pin: int = 27
    left_enable_pin: int = 22
    right_forward_pin: int = 23
    right_backward_pin: int = 24
    right_enable_pin: int = 25
    servo_pin: int = 18

@dataclass
class DisplayConfig:
    width: int = 800
    height: int = 480
    fullscreen: bool = False
    fps: int = 60

@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 5000
    enable_auth: bool = False
    api_key: str = ""

@dataclass
class SysBotConfig:
    audio: AudioConfig
    voice: VoiceConfig
    motor: MotorConfig
    display: DisplayConfig
    api: APIConfig

    @classmethod
    def from_file(cls, path: str) -> "SysBotConfig":
        """Load configuration from YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(
            audio=AudioConfig(**data.get('audio', {})),
            voice=VoiceConfig(**data.get('voice', {})),
            motor=MotorConfig(**data.get('motor', {})),
            display=DisplayConfig(**data.get('display', {})),
            api=APIConfig(**data.get('api', {}))
        )
```

---

### 8. Main Application

```python
# src/main.py

import asyncio
from config import SysBotConfig
from voice.audio_manager import AudioManager
from voice.wake_word import WakeWordDetector
from voice.stt import WhisperLocalSTT
from voice.llm import OllamaLLM
from voice.tts import PiperTTS
from voice.conversation import ConversationManager
from display.renderer import DisplayRenderer
from vision.camera import Camera
from vision.detector import PersonDetector
from vision.tracker import PersonTracker
from motion.motor_controller import MotorController
from motion.servo_controller import ServoController
from motion.follow_me import FollowMeController
from api.server import run_server
from utils.events import EventBus, Event

class SysBot:
    """Main SysBot application."""

    def __init__(self, config_path: str = "config/default.yaml"):
        self.config = SysBotConfig.from_file(config_path)
        self.event_bus = EventBus()

        # Initialize modules
        self.audio = AudioManager(self.config.audio)
        self.wake_word = WakeWordDetector(self.config.voice.wake_word)
        self.stt = WhisperLocalSTT(self.config.voice.stt_model)
        self.llm = OllamaLLM(self.config.voice.llm_model)
        self.tts = PiperTTS(self.config.voice.tts_voice)
        self.conversation = ConversationManager(self.stt, self.llm, self.tts)
        self.display = DisplayRenderer(
            self.config.display.width,
            self.config.display.height
        )
        self.camera = Camera()
        self.detector = PersonDetector()
        self.tracker = PersonTracker()
        self.motor = MotorController(self.config.motor)
        self.servo = ServoController(self.config.motor.servo_pin)
        self.follow = FollowMeController(self.motor, self.servo)

        # Set up event handlers
        self._setup_events()

    def _setup_events(self):
        """Set up event handlers."""
        self.event_bus.subscribe(Event.WAKE_WORD_DETECTED,
                                  lambda _: self.display.set_state('listening'))
        self.event_bus.subscribe(Event.LLM_RESPONSE_START,
                                  lambda _: self.display.set_state('thinking'))
        self.event_bus.subscribe(Event.TTS_START,
                                  lambda _: self.display.set_state('speaking'))
        self.event_bus.subscribe(Event.TTS_END,
                                  lambda _: self.display.set_state('idle'))

    async def run(self):
        """Run all SysBot tasks."""
        tasks = [
            self._voice_loop(),
            self._display_loop(),
            self._vision_loop(),
            self._api_server(),
        ]
        await asyncio.gather(*tasks)

    async def _voice_loop(self):
        """Main voice assistant loop."""
        while True:
            # Wait for wake word
            audio_stream = self.audio.start_recording()
            await self.wake_word.listen(audio_stream)

            # Wake word detected
            await self.event_bus.emit(Event.WAKE_WORD_DETECTED)

            # Record user speech
            user_audio = await self.audio.record_until_silence()

            # Process conversation
            await self.conversation.process(user_audio, self.audio)

    async def _display_loop(self):
        """Display animation loop."""
        await self.display.run()

    async def _vision_loop(self):
        """Vision and follow-me loop."""
        while True:
            frame = self.camera.get_frame()
            if frame is not None:
                detection = self.detector.detect(frame)
                tracking = self.tracker.update(detection)
                self.follow.update(tracking)
            await asyncio.sleep(0.033)  # ~30 FPS

    async def _api_server(self):
        """Run API server in background."""
        import threading
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    bot = SysBot()
    asyncio.run(bot.run())
```

---

## GPIO Pin Mapping

**Motor Driver (Cunyuer DC5 12V Dual Channel H Bridge):**

| Pin | GPIO | Function |
|-----|------|----------|
| 11 | GPIO17 | Left Motor IN1 |
| 13 | GPIO27 | Left Motor IN2 |
| 15 | GPIO22 | Left Motor Enable (PWM) |
| 16 | GPIO23 | Right Motor IN1 |
| 18 | GPIO24 | Right Motor IN2 |
| 22 | GPIO25 | Right Motor Enable (PWM) |

**I2C Bus (for PCA9685 Servo Driver & WM8960 Audio HAT):**

| Pin | GPIO | Function |
|-----|------|----------|
| 3 | GPIO2 | I2C SDA |
| 5 | GPIO3 | I2C SCL |

**PCA9685 PWM Channels:**

| Channel | Function |
|---------|----------|
| 0 | MG996R Head Servo (pan) |

---

## Communication Protocols

### Mobile App ↔ Robot

**WebSocket Events:**

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `connect` | App → Robot | - | Initial connection |
| `move` | App → Robot | `{x: float, y: float}` | Joystick movement |
| `servo` | App → Robot | `{angle: float}` | Head servo angle |
| `stop` | App → Robot | - | Emergency stop |
| `mode` | App → Robot | `{mode: string}` | Set mode |
| `status` | Robot → App | `{mode, battery, ...}` | Status update |
| `error` | Robot → App | `{message: string}` | Error notification |

---

## Dependencies

### Python Packages

```txt
# requirements.txt

# Core
python>=3.11

# Audio
pyaudio>=0.2.13
sounddevice>=0.4.6
numpy>=1.24.0

# Wake Word
openwakeword>=0.5.0

# Speech-to-Text
faster-whisper>=0.9.0

# LLM
ollama>=0.1.0
openai>=1.0.0  # Optional

# Text-to-Speech
piper-tts>=1.2.0
edge-tts>=6.1.0  # Optional

# Display
pygame>=2.5.0

# Vision
opencv-python>=4.8.0
mediapipe>=0.10.0

# GPIO
gpiozero>=2.0.0
pigpio>=1.78
adafruit-circuitpython-pca9685>=3.4.0  # PCA9685 I2C servo driver
adafruit-circuitpython-servokit>=1.3.0  # Servo control helper

# API Server
flask>=3.0.0
flask-socketio>=5.3.0
flask-cors>=4.0.0

# Utilities
pyyaml>=6.0.0
```

---

## Security Considerations

1. **Network Security:**
   - Use HTTPS for API server in production
   - Implement API key authentication
   - Limit API access to local network

2. **Physical Safety:**
   - Implement hardware emergency stop
   - Add collision detection sensors
   - Set speed limits on motors
   - Timeout on lost connection

3. **Privacy:**
   - Process audio locally when possible
   - Don't store conversations permanently
   - Secure camera feed access

---

## Testing Strategy

1. **Unit Tests:** Test individual modules in isolation
2. **Integration Tests:** Test module interactions
3. **Hardware-in-Loop:** Test with actual hardware
4. **End-to-End:** Full system tests

---

## Performance Targets

| Metric | Target |
|--------|--------|
| Wake word latency | < 500ms |
| STT latency | < 1s (local) |
| LLM response start | < 2s (local) |
| TTS latency | < 500ms |
| Display FPS | 60 FPS |
| Vision FPS | 30 FPS |
| Control latency | < 50ms |

---

## Next Steps

1. Review this architecture document
2. Proceed to [02-roadmap.md](02-roadmap.md) for development milestones
3. Set up development environment on Raspberry Pi 5
4. Begin with Milestone 1.1: Environment Setup
