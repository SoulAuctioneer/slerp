import pygame
import pygame_functions as pyg
from .service_locator import ServiceLocator
import os

AUDIO_DIR = 'assets/audio'

class Audio:
    def __init__(self):
        self._event_manager = ServiceLocator.get("event_manager")
        self._event_manager.subscribe("PLAY_AUDIO", self.play)
        self._event_manager.subscribe("STOP_AUDIO", self.stop)
        self._event_manager.subscribe("QUEUE_AUDIO", self.enqueue)
        self._event_manager.subscribe("PLAY_MUSIC", self.play_music)
        self._event_manager.subscribe("STOP_MUSIC", self.stop_music)

        self.audio_files = {}
        self.playing_audio = None
        self.queue = []
        self.load_audio_files()

    def load_audio_files(self):
        for file in os.listdir(AUDIO_DIR):
            if file.endswith(('.mp3', '.wav')):
                audio_name = os.path.splitext(file)[0]
                audio_path = os.path.join(AUDIO_DIR, file)
                self.audio_files[audio_name] = pyg.makeSound(audio_path)

    def play(self, name, loops=0, on_complete=None, **kwargs):
        self.stop()
        if name in self.audio_files:
            self.playing_audio = self.audio_files[name]
            self.playing_audio.play(loops)
        return self.playing_audio

    def play_music(self, name, loops=-1, volume=1.0):
        pyg.makeMusic(os.path.join(AUDIO_DIR, f"{name}.mp3"))
        # Set volume (0.0 to 1.0)
        pygame.mixer.music.set_volume(volume)
        pyg.playMusic(loops)

    def stop_music(self):
        pyg.stopMusic()

    def stop(self):
        if self.playing_audio:
            self.playing_audio.stop()
            self.playing_audio = None

    def enqueue(self, name):
        if name in self.audio_files:
            self.queue.append(name)
            return self.audio_files[name]

    def play_next_in_queue(self):
        if self.queue:
            next_name = self.queue.pop(0)
            self.play(next_name)

    def refresh(self):
        # This is a bit of a hack since pygame.mixer doesn't have a reliable "is_busy" for sounds.
        # We'll assume if the main mixer is not busy, our sound is done.
        # A better implementation might use channels.
        if self.playing_audio and not pygame.mixer.get_busy():
            self.playing_audio = None
            self.play_next_in_queue()
