from .base import Scene
from .scene_six import SceneSix

class SceneFive(Scene):
    def run(self):
        '''
        SCENE 5
        Slerp: But it's not just any icy confection. This stuff is special: <whispers sotto voce> I add Ascension Factor X! It's this incredible alien cumcoction, gifted to us by our alien benefactors, and you definitely want it! <exasperated> Although I am legally required to receive your consent to add the Factor X to your slushie. 
        > Go to SCENE 6
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene5')
        self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTalking)
        self.context.event_scheduler.schedule(clip.get_length(), lambda: self.context.set_scene(SceneSix(self.context)))
        self.context.dispenser.schedule_bubble(1, 'cyan', 4)
        self.context.dispenser.schedule_bubble(5, 'magenta', 5)
        self.context.dispenser.schedule_bubble(10, 'yellow', 5)
        self.context.dispenser.schedule_bubble(12, 'transparent', 5) 