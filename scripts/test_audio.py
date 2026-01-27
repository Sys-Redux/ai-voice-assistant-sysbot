import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.voice.audio_manager import AudioManager
from src.utils.logger import setup_logger

async def test_list_devices(audio: AudioManager):
    print("\n=== Testing: List Audio Devices ===")
    for device in audio.list_devices():
        direction = []
        if device["inputs"] > 0:
            direction.append(f"IN:{device['inputs']}")
        if device["outputs"] > 0:
            direction.append(f"OUT:{device['outputs']}")
        print(f" [{device['index']}] {device['name']} ({', '.join(direction)})")
    print()

async def test_recording(audio: AudioManager, duration: float = 3.0):
    print(f"\n=== Testing: Recording Audio for {duration} seconds ===")
    await audio.start()

    chunks = []
    start_time = asyncio.get_event_loop().time()

    async for chunk in audio.stream_audio():
        chunks.append(chunk)
        elapsed = asyncio.get_event_loop().time() - start_time
        level = audio.get_audio_level()
        bar = "█" * int(level * 50)
        print(f"\r  Level: [{bar:<50}] {level:.2f}", end="", flush=True)

        if elapsed >= duration:
            break

    await audio.stop()
    print("\nRecording complete. Number of chunks recorded:", len(chunks))
    return b"".join(chunks)

async def test_playback(audio: AudioManager, audio_data: bytes):
    print("\n=== Testing: Audio Playback ===")
    await audio.play_audio(audio_data)
    print("Playback complete.")

async def main():
    logger = setup_logger("sysbot", log_file="lpgs/test_audio.log")
    logger.info("Starting audio tests...")

    config = Config.load()
    audio = AudioManager(config.audio)

    await test_list_devices(audio)
    recorded = await test_recording(audio, duration=3.0)
    if recorded:
        await test_playback(audio, recorded)

    print("\nAll tests completed.")

if __name__ == "__main__":
    asyncio.run(main())