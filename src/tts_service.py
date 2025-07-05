import asyncio
import threading
import pygame
from .service_locator import ServiceLocator
from .speech_synthesiser import SpeechSynthesizer
from .settings import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, ELEVENLABS_MODEL_ID, TTS_CACHE_DIR

class TTSService:
    def __init__(self):
        self._event_manager = ServiceLocator.get("event_manager")
        self._event_manager.subscribe("SYNTHESIZE_SPEECH", self.synthesize_speech)
        self._event_manager.subscribe("STOP_SPEECH", self.stop_speech)
        
        # Initialize speech synthesizer if API key is available
        if ELEVENLABS_API_KEY:
            self.synthesizer = SpeechSynthesizer(
                api_key=ELEVENLABS_API_KEY,
                voice_id=ELEVENLABS_VOICE_ID,
                model_id=ELEVENLABS_MODEL_ID,
                cache_dir=TTS_CACHE_DIR
            )
        else:
            self.synthesizer = None
            print("WARNING: ELEVENLABS_API_KEY not set, TTS will not work")
        
        self.current_sound = None
        self.current_callback = None

    def synthesize_speech(self, text, callback=None, voice_id=None, model_id=None, **kwargs):
        """Handle SYNTHESIZE_SPEECH event by running async synthesis in a separate thread"""
        if not self.synthesizer:
            print("TTS: No synthesizer available, skipping speech synthesis")
            if callback:
                callback()
            return
        
        self.current_callback = callback
        
        # Run the async synthesis in a separate thread using asyncio.run()
        thread = threading.Thread(
            target=self._run_synthesis_thread,
            args=(text, voice_id, model_id)
        )
        thread.start()

    def _run_synthesis_thread(self, text, voice_id, model_id):
        """Run the async synthesis in a separate thread using asyncio.run()"""
        try:
            # Use asyncio.run() which handles event loop lifecycle automatically
            audio_path = asyncio.run(
                self.synthesizer.synthesize_speech(text, voice_id, model_id)
            )
            
            if audio_path:
                # Play the audio using pygame
                self._play_audio_file(str(audio_path))
            else:
                print("TTS: Failed to synthesize speech")
                if self.current_callback:
                    self.current_callback()
                    
        except Exception as e:
            print(f"TTS: Error in synthesis thread: {e}")
            if self.current_callback:
                self.current_callback()

    def _play_audio_file(self, audio_path):
        """Play the audio file using pygame"""
        try:
            pygame.mixer.init()
            self.current_sound = pygame.mixer.Sound(audio_path)
            self.current_sound.play()
            print(f"TTS: Playing synthesized speech from {audio_path}")
            
            # Get exact speech duration and publish event
            sound_length = self.current_sound.get_length()
            self._event_manager.publish("SPEECH_STARTED", duration=sound_length)
            
            # Schedule callback when sound finishes
            if self.current_callback:
                # Use pygame's event system to schedule the callback
                event_scheduler = ServiceLocator.get("event_scheduler")
                event_scheduler.schedule(sound_length, self.current_callback)
                
        except Exception as e:
            print(f"TTS: Error playing audio file: {e}")
            if self.current_callback:
                self.current_callback()

    def stop_speech(self):
        """Stop currently playing speech"""
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None 