import pygame
from .base import Scene
from ..button import Button
from .scene_nine import SceneNine

class SceneEight(Scene):
    def run(self):
        '''
        SCENE 8
        Slerp: Thank you for your consent! Isn’t the illusion of free will fabulous?!
        Ascension Factor X is the sacrament of our alien benefactors, the Elders of Nebula (pronounced “nrrblrr”). While preparing your soul for Ascension, it also has the happy side effect of instantly granting you an incredible superpower of your choice!
        Place a cup below the dispenser. Be careful, I’m very delicate.
        UI:
        Done > Go to SCENE 9
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene8')
        delay = self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTalking)
        self.context.schedule_idling(clip.get_length())
        buttons = [
            Button(self.context.screen, pygame.Rect(100, 300, 520, 240), "OK", (255, 0, 255), lambda: self.context.set_scene(SceneNine(self.context)))
        ]
        self.context.event_scheduler.schedule(22, self.context.set_buttons, buttons) 