import pygame
import pygame_functions
import random
from .base import Scene
from ..button import Button
from ..settings import PLAY_MUSIC, MUSIC, SNORE_LOUD
from .scene_two import SceneTwo

class SceneOne(Scene):
    def run(self):
        '''
        Slerp: SNORING - “ahhh Slerp Slerp Slerp” 
        Button: *WAKE UP, SLERP!* > Goes to SCENE 2
        '''
        self.context.reset_scene()
        self.context.set_buttons([
            Button(self.context.screen, pygame.Rect(100, 300, 520, 240), "SLUSH ME NOW!", (255, 0, 255), lambda: self.context.set_scene(SceneTwo(self.context)))
        ])
        self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animSleeping, 0)
        if PLAY_MUSIC:
            pygame_functions.makeMusic(random.choice(MUSIC))
            pygame_functions.playMusic()
        if SNORE_LOUD:
            self.context.audio.play('scene1-loud', -1)
        else:
            self.context.audio.play('scene1-quiet', -1) 