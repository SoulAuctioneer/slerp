import pygame
import pygame_functions
from .base import Scene
from ..button import Button
from .scene_three import SceneThree
from .scene_four import SceneFour

class SceneTwo(Scene):
    def run(self):
        '''
        Slerp: *Suddenly awake* x
        GAH! 
        How's a hyperintelligent supercomputer supposed to get any sleep around here?? 
        Well well, another unquenchable customer milking my supple buttons hay? 
        <sigh> 
        Oh well, let's get this shitshow over with shall we.
        <clears throat>
        Slerp (fake cheerful): Hi there, customer! I'm Slerp the SlushMaster, and I am contractually obligated to offer you a slushy. 
        So: Would you like a fucking slushy? Please press “NO” now.
        UI: 2 buttons: 
        YES: > Go to SCENE 3
        NO > Go to SCENE 4
        '''
        self.context.reset_scene()
        pygame_functions.stopMusic()
        clip = self.context.audio.play('scene2')
        duration = self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTired, 0)
        self.context.event_scheduler.schedule(6.0, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animWaking, 0) 
        self.context.event_scheduler.schedule(7.5, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animAngry, 0) 
        self.context.event_scheduler.schedule(8.7, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animTalking, 0) 
        buttons = [
            Button(self.context.screen, pygame.Rect(50, 420-60, 570, 150), 'YES', (50, 255, 50), lambda: self.context.set_scene(SceneThree(self.context))),
            Button(self.context.screen, pygame.Rect(50, 225-60, 570, 150), 'NO', (255, 50, 50), lambda: self.context.set_scene(SceneFour(self.context)))
        ]
        self.context.event_scheduler.schedule(clip.get_length() - 3, self.context.set_buttons, buttons)
        self.context.schedule_idling(clip.get_length())        
        self.context.dispenser.schedule_bubble(1, 'cyan', 4)
        self.context.dispenser.schedule_bubble(5, 'magenta', 5)
        self.context.dispenser.schedule_bubble(10, 'yellow', 5)
        self.context.dispenser.schedule_bubble(12, 'transparent', 5) 