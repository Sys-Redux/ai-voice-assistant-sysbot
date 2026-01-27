from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class AudioConfig:
    sample_rate: int = 16000
    chunk_size: int = 1024
    channelsL: int = 1
    input_device: str | None = None
    output_device: str | None = None

@dataclass
class Config:
    """Main config container"""
    audio: AudioConfig

    @classmethod
    def load(cls, path: str = "config/default.yaml") -> "Config":
        config_path = Path(path)
        if not config_path.exists():
            with open(config_path) as f:
                data = yaml.safe_load(f)
            return cls(
                audio=AudioConfig(**data.get("audio", {}))
            )
        return cls(audio=AudioConfig())