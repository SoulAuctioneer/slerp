import pygame
from .base import Scene
from ..button import Button
from .scene_seven import SceneSeven
from .scene_eight import SceneEight

class SceneSix(Scene):
    def run(self):
        '''
        SCENE 6
        Slerp: Press “I consent” now, please.
        UI: 
        I CONSENT > Go to SCENE 8
        I DO NOT CONSENT > Go to SCENE 7
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene6')
        delay = self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTalking)
        self.context.schedule_idling(clip.get_length())
        self.context.set_buttons([
            Button(self.context.screen, pygame.Rect(50, 225-60, 570, 150), 'I CONSENT', (50, 255, 50), lambda: self.context.set_scene(SceneEight(self.context))),
            Button(self.context.screen, pygame.Rect(50, 420-60, 570, 150), 'I DO NOT CONSENT', (255, 50, 50), lambda: self.context.set_scene(SceneSeven(self.context)))
        ]) 