from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class AudioConfig:
    sample_rate: int = 16000
    chunk_size: int = 1024
    channels: int = 1
    input_device: str | None = None
    output_device: str | None = None

@dataclass
class WakeWordConfig:
    """Wake word detection config"""
    engine: str = "openwakeword"
    model_path: str | None = None # To custom .onnx model
    sensitivity: float = 0.5 # Detection threshold
    wake_word: str = "hey_sysbot"
    inference_framework: str = "onnx" # Or "tflite"
    cooldown: float = 2.0

@dataclass
class Config:
    """Main config container"""
    audio: AudioConfig
    wake_word: WakeWordConfig

    @classmethod
    def load(cls, path: str = "config/default.yaml") -> "Config":
        config_path = Path(path)
        if not config_path.exists():
            with open(config_path) as f:
                data = yaml.safe_load(f)
            return cls(
                audio=AudioConfig(**data.get("audio", {})),
                wake_word=WakeWordConfig(**data.get("wake_word", {}))
            )
        return cls(audio=AudioConfig(), wake_word=WakeWordConfig())