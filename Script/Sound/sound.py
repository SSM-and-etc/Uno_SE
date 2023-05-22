import pygame

import os

class Sound():
    def __init__(self, main):
        root = main.root_path
        self.user_data = main.user_data
        self.now_stage_idx = 0
        self.set_sounds(root)
        self.set_volume()
        self.bgms[self.now_stage_idx].play(-1)
        
    def set_sounds(self, root):
        self.set_effect(root)
        self.set_bgm(root)
        
    def set_effect(self, root):
        self.card_selection = pygame.mixer.Sound(os.path.join(root, "Material/Sound/card_selection.ogg"))
        self.card_submission = pygame.mixer.Sound(os.path.join(root, "Material/Sound/card_submission.ogg"))
    
    def set_bgm(self, root):
        funkysuspense = pygame.mixer.Sound(os.path.join(root, "Material/Sound/funkysuspense.ogg"))
        downtown = pygame.mixer.Sound(os.path.join(root, "Material/Sound/downtown.ogg"))
        energy = pygame.mixer.Sound(os.path.join(root, "Material/Sound/energy.ogg"))
        hey = pygame.mixer.Sound(os.path.join(root, "Material/Sound/hey.ogg"))
        
        self.bgms = \
        [
            funkysuspense,
            energy,
            downtown,
            hey,
            downtown,
            energy,
            hey
        ]
        
    def set_volume(self):
        if self.user_data.volumes_off[0]:
            self.set_effect_volume(0)
            self.set_bgm_volume(0)
        else: 
            self.set_bgm_volume(self.user_data.volumes[0] * self.user_data.volumes[1])
            self.set_effect_volume(self.user_data.volumes[0] * self.user_data.volumes[2])
            
    def set_bgm_volume(self, volume):
        if self.user_data.volumes_off[1]:
            volume = 0
        for bgm in self.bgms:
            bgm.set_volume(volume)
    
    def set_effect_volume(self, volume):
        if self.user_data.volumes_off[2]:
            volume = 0
        self.card_selection.set_volume(volume)
        self.card_submission.set_volume(volume)
            
    def change_bgm(self, stage_idx):
        self.bgms[self.now_stage_idx].fadeout(2)
        self.bgms[stage_idx].play(-1)
        self.now_stage_idx = stage_idx