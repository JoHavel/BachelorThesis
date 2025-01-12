from mashcima import Mashcima
from mashcima.canvas_items.StemNote import StemNote
import random
import copy
import numpy as np


class FlagNote(StemNote):
    def __init__(self, flag_kind: str, **kwargs):
        super().__init__(**kwargs)

        assert flag_kind in ["e", "s"]
        self.kind = flag_kind

    def get_note_generic_annotation(self) -> str:
        return self.kind

    def select_sprites(self, mc: Mashcima):
        if self.kind == "e":
            self.sprites = copy.deepcopy(random.choice(mc.EIGHTH_NOTES))
            from mashcima import SpriteGroup
            if not isinstance(self.sprites, SpriteGroup):
                # decide whether to flip or not, copied from super().select_sprites
                self.flipped = self.pitch > 0
                if self.pitch in self.canvas_options.randomize_stem_flips_for_pitches:
                    self.flipped = random.choice([True, False])
                self.sprites = self.sprites[0 if self.flipped else 1]
            # And we call Grandparent's super
            super(StemNote, self).select_sprites(mc)
            return

        if self.kind == "s":
            self.sprites = copy.deepcopy(random.choice(mc.SIXTEENTH_NOTES))
        super().select_sprites(mc)

    def place_sprites(self):
        super().place_sprites()

        if self.flipped:
            if self.sprites.has_sprite("flag_8"):
                f = self.sprites.sprite("flag_8")
                f.mask = np.flip(f.mask, axis=1)
                f.x += f.width

            if self.kind == "s" and self.sprites.has_sprite("flag_16"):
                f = self.sprites.sprite("flag_16")
                f.mask = np.flip(f.mask, axis=1)
                f.x += f.width
