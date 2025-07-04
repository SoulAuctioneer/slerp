from .base import Scene
from .scene_eight import SceneEight

class SceneFour(Scene):
    def run(self):
        '''
        SCENE 4
        Slerp: Ahh yes your compliant nature makes you a perfect candidate for Ascension! In that case, I shall entirely disregard your preference, and for your own good I SHALL serve you a slushy.
        > Go to SCENE 5
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene4')
        self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTalking)
        self.context.event_scheduler.schedule(clip.get_length(), lambda: self.context.set_scene(SceneEight(self.context))) 