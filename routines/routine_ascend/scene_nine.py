from .base import Scene

class SceneNine(Scene):
    def run(self):
        '''
        SCENE 9
        What superpower shall I mix into your alien slushy?
        UI:
        Invisibility > Go to SCENE 10 (orange)
        Teleportation > Go to SCENE 11 (purple)
        Telekinesis > Go to SCENE 12 (yellow)
        Clairvoyance > Go to SCENE 13 (green)
        Omnilingualism > Go to SCENE 14 (blue)
        Flight > Go to SCENE 15 (red)
        '''
        self.context.reset_scene()
        clip = self.context.audio.play('scene9')
        delay = self.context.slerp_sprite.start_anim(self.context.slerp_sprite.animTalking)
        self.context.schedule_idling(clip.get_length())
        self.context.show_drink_buttons() 