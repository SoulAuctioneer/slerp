import asyncio
import hashlib
import logging
import os
from pathlib import Path
from typing import Optional

from elevenlabs.client import AsyncElevenLabs
import aiofiles

# Basic logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechSynthesizer:
    """
    Manages Text-to-Speech synthesis using ElevenLabs, with caching.
    """
    def __init__(self, api_key: str, voice_id: str, model_id: str, cache_dir: str = "assets/tts_cache"):
        if not api_key:
            raise ValueError("ElevenLabs API key is required.")
        
        self.api_key = api_key
        self.default_voice_id = voice_id
        self.default_model_id = model_id
        
        self._async_client = AsyncElevenLabs(api_key=self.api_key)
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(exist_ok=True)
        logger.info(f"SpeechSynthesizer initialized. Cache directory: {self._cache_dir.absolute()}")

    def _generate_cache_key(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> str:
        """Generate a unique cache key based on text and TTS parameters."""
        voice_id = voice_id or self.default_voice_id
        model_id = model_id or self.default_model_id
        
        cache_string = f"{text}|{voice_id}|{model_id}"
        hash_object = hashlib.sha256(cache_string.encode('utf-8'))
        return hash_object.hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get the full path for a cached audio file."""
        return self._cache_dir / f"{cache_key}.mp3"

    async def _check_cache(self, cache_key: str) -> Optional[Path]:
        """Check if audio is cached and return its path if available."""
        cache_path = self._get_cache_path(cache_key)
        if cache_path.exists():
            logger.info(f"Cache hit for key: {cache_key}")
            return cache_path
        logger.info(f"Cache miss for key: {cache_key}")
        return None

    async def synthesize_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
    ) -> Optional[Path]:
        """
        Synthesizes speech from text, saves it to a file, and returns the path.
        Checks cache first. If not found, generates audio using ElevenLabs API,
        caches it, and then returns the path.
        """
        voice_id = voice_id or self.default_voice_id
        model_id = model_id or self.default_model_id

        cache_key = self._generate_cache_key(text, voice_id, model_id)
        cached_path = await self._check_cache(cache_key)
        if cached_path:
            return cached_path

        logger.info(f"Generating audio stream for text: '{text[:30]}...'")
        
        try:
            audio_stream = await self._async_client.text_to_speech.stream(
                text=text,
                voice_id=voice_id,
                model_id=model_id,
                output_format="mp3_44100_128" # Use mp3 format
            )

            all_audio_chunks = []
            async for audio_chunk_bytes in audio_stream:
                if audio_chunk_bytes:
                    all_audio_chunks.append(audio_chunk_bytes)
            
            if not all_audio_chunks:
                logger.error("TTS stream was empty, no audio data received.")
                return None

            combined_audio = b''.join(all_audio_chunks)
            
            cache_path = self._get_cache_path(cache_key)
            async with aiofiles.open(cache_path, 'wb') as f:
                await f.write(combined_audio)
            
            logger.info(f"Saved synthesized audio to cache: {cache_path}")
            return cache_path

        except Exception as e:
            logger.error(f"Error generating or saving audio stream from ElevenLabs: {e}", exc_info=True)
            return None

if __name__ == '__main__':
    # Example usage, requires ELEVENLABS_API_KEY environment variable
    async def main():
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("Please set the ELEVENLABS_API_KEY environment variable.")
            return

        synthesizer = SpeechSynthesizer(
            api_key=api_key,
            voice_id="21m00Tcm4TlvDq8ikWAM", # Example voice ID for Rachel
            model_id="eleven_multilingual_v2"
        )
        
        text_to_speak = "Hello from Slerp the SlushMaster! Would you like a slushie?"
        
        print(f"Synthesizing speech for: '{text_to_speak}'")
        audio_path = await synthesizer.synthesize_speech(text_to_speak)
        
        if audio_path:
            print(f"Speech synthesized and saved to: {audio_path}")
            # Here you would typically use a library like pygame to play the audio file.
            # For example:
            # pygame.mixer.init()
            # pygame.mixer.music.load(audio_path)
            # pygame.mixer.music.play()
            # while pygame.mixer.music.get_busy():
            #     pygame.time.Clock().tick(10)
        else:
            print("Failed to synthesize speech.")

    asyncio.run(main()) 