from .base import Scene
from .scene_one import SceneOne

class SceneEleven(Scene):
    def run(self):
        '''
        Unfortunately I now have to sing the jingle
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene16')
        self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTalking, 0)
        self.context.event_scheduler.schedule(8, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animSinging)
        self.context.event_scheduler.schedule(13.8, self.context.slerp_sprite.start_anim, self.context.slerp_sprite.animTired)
        self.context.event_scheduler.schedule(clip.get_length(), lambda: self.context.set_scene(SceneOne(self.context))) 