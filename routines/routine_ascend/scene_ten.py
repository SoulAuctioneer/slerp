import pygame_functions
from .base import Scene
from ..settings import BG_IMAGE, BG_IMAGE_SYMBOL
from .scene_eleven import SceneEleven

class SceneTen(Scene):
    def __init__(self, context, drink_name):
        super().__init__(context)
        self.drink_name = drink_name

    def run(self):
        '''
        SCENE 10 - drinkies 
        Slerp: One cosmic juice coming right up!
        ...
        '''
        self.context.reset_scene()
        pygame_functions.setBackgroundImage(BG_IMAGE_SYMBOL)
        timer = 0
        clip = self.context.audio.play('scene10-1')
        timer += clip.get_length()
        clip = self.context.audio.enqueue('scene10-2-%s' % self.drink_name)
        timer += clip.get_length()
        timer_start_straining = timer
        clip = self.context.audio.enqueue('scene10-3')
        timer += clip.get_length()
        timer_start_superpower_disclaimer = timer
        clip = self.context.audio.enqueue('scene10-4-%s' % self.drink_name)
        timer += clip.get_length()
        timer_end_scene = timer
        self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTalking, 0)
        self.context.event_scheduler.schedule(timer_start_straining, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animStraining)
        self.context.event_scheduler.schedule(4, self.context.dispenser.dispense, self.context.drinks[self.drink_name])
        self.context.event_scheduler.schedule(timer_start_straining + 11, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animTired)
        self.context.event_scheduler.schedule(timer_start_straining + 30, pygame_functions.setBackgroundImage, BG_IMAGE) 
        self.context.event_scheduler.schedule(timer_start_superpower_disclaimer, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animTalking)
        self.context.event_scheduler.schedule(timer_end_scene, lambda: self.context.set_scene(SceneEleven(self.context))) 