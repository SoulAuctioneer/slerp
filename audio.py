import os
import pygame
import pygame_functions as pyg

AUDIO_DIR = 'assets/audio'

class Audio:

    def __init__(self):
        self.audio_files = {}
        self.playing_audio = None
        self.queue = []
        self.load_audio_files()

    def load_audio_files(self):
        for file in os.listdir(AUDIO_DIR):
            if file.endswith(('.mp3', '.wav')):
                audio_name = os.path.splitext(file)[0]  # Get the name of the audio file without extension
                audio_path = os.path.join(AUDIO_DIR, file)
                self.audio_files[audio_name] = pyg.makeSound(audio_path)

    def play(self, name, loops=0):
        self.stop()
        if name in self.audio_files:
            self.playing_audio = self.audio_files[name]
            self.playing_audio.play(loops)
        return self.playing_audio

    def stop(self):
        if self.playing_audio:
            self.playing_audio.stop()

    def enqueue(self, name):
        if name in self.audio_files:
            self.queue.append(name)
            return self.audio_files[name]

    def play_next_in_queue(self):
        if self.queue:
            next_name = self.queue.pop(0)
            print(f"Playing audio file: {next_name}")
            self.play(next_name)

    def refresh(self):
        if not pygame.mixer.get_busy():
            self.playing_audio = None
            self.play_next_in_queue()
