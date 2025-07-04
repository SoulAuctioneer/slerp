from .base import Scene
from .scene_eight import SceneEight

class SceneThree(Scene):
    def run(self):
        '''
        SCENE 3
        Slerp: Fine, fine, brain the size of a planet and they've got me excreting frozen goop.
        > Go to SCENE 5
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene3')
        self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animAngry)
        self.context.event_scheduler.schedule(clip.get_length(), lambda: self.context.set_scene(SceneEight(self.context))) 