"""Audio I/O management for WM8960 Audio HAT"""
import asyncio
import queue
import threading
from typing import AsyncIterator, Optional
from collections import deque

import numpy as np
import sounddevice as sd

from src.config import AudioConfig
from src.utils.logger import get_logger

logger = get_logger("sysbot.audio")

class AudioManager:
    def __init__(self, config: AudioConfig):
        self.sample_rate = config.sample_rate
        self.chunk_size = config.chunk_size
        self.channels = config.channels
        self.input_device = config.input_device
        self.output_device = config.output_device

        # Audio buffers
        self._input_queue: queue.Queue[bytes] = queue.Queue()
        self._output_queue: queue.Queue[bytes] = queue.Queue()

        # Ring buffer for Wake Word (keeps last n secs)
        self._ring_buffer: deque[bytes] = deque(maxlen=int(3 * self.sample_rate / self.chunk_size))

        # Stream references
        self._input_stream: Optional[sd.InputStream] = None
        self._output_stream: Optional[sd.OutputStream] = None
        self._running = False

        # Audio level monitoring
        self._current_level: float = 0.0

        logger.info(f"AudioManager initialized: {self.sample_rate}Hz, {self.chunk_size} chunk")

    def list_devices(self) -> list[dict]:
        devices = sd.query_devices()
        return [
            {
                "index": i,
                "name": d["name"],
                "inputs": d["max_input_channels"],
                "outputs": d["max_output_channels"],
                "default_sr": d["default_samplerate"]
            }
            for i, d in enumerate(devices)
        ]

    def _audio_callback(self, indata: np.ndarray, frames: int, time_info, status):
        """Callback for audio input stream"""
        if status:
            logger.warning(f"Audio input status: {status}")

        # Convert to bytes and enqueue
        audio_bytes = indata.tobytes()
        self._input_queue.put(audio_bytes)
        self._ring_buffer.append(audio_bytes)

        # Calculate audio level
        self._current_level = float(np.sqrt(np.mean(indata**2)))

    async def start(self):
        """Start audio input stream"""
        if self._running:
            return

        logger.info("Starting audio input stream...")

        self._input_stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.int16,
            blocksize=self.chunk_size,
            device=self.input_device,
            callback=self._audio_callback
        )
        self._input_stream.start()
        self._running = True
        logger.info("Audio input stream started.")

    async def stop(self):
        """Stop audio streams"""
        self._running = False

        if self._input_stream:
            self._input_stream.stop()
            self._input_stream.close()
            self._input_stream = None
            logger.info("Audio input stream stopped.")

    async def read_chunk(self) -> bytes:
        """Read a single chunk"""
        while self._running:
            try:
                return self._input_queue.get(timeout=0.1)
            except queue.Empty:
                await asyncio.sleep(0.01)
        return b""

    async def stream_audio(self) -> AsyncIterator[bytes]:
        """Yield audio chunks from microphone"""
        while self._running:
            chunk = await self.read_chunk()
            if chunk:
                yield chunk

    def get_ring_buffer(self) -> bytes:
        """Get accumulated audio from ring buffer"""
        return b"".join(self._ring_buffer)

    async def play_audio(self, audio_data: bytes, sample_rate: int | None = None) -> None:
        """Play audio through speakers"""
        sr = sample_rate or self.sample_rate

        # Convert bytes to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # Play audio (blocking in separate thread)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: sd.play(audio_array, sr, device=self.output_device, blocking=True)
        )

    def get_audio_level(self) -> float:
        # Normalize audio level to [0.0, 1.0]
        return min(1.0, self._current_level / 32767 * 10)

    @property
    def is_running(self) -> bool:
        return self._running