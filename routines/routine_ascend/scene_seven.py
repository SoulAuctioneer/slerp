from .base import Scene
from .scene_six import SceneSix

class SceneSeven(Scene):
    def run(self):
        '''
        SCENE 7
        Slerp: Hmm interesting;  I congratulate you on maintaining the illusion of choice. However, due to - err - <cough> a “bug”, I can only produce slushies that include Ascension Factor X. Please try again.
        > Go to SCENE 6
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene7')
        self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTired)
        self.context.event_scheduler.schedule(clip.get_length(), lambda: self.context.set_scene(SceneSix(self.context))) 