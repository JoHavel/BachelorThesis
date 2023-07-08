from mashcima import Mashcima
from mashcima.canvas_items.QuarterNote import QuarterNote
import copy


class BeamedNote(QuarterNote):
    def __init__(
            self,
            beams: int,
            left_beamed: bool,
            right_beamed: bool,
            **kwargs
    ):
        super().__init__(**kwargs)
        assert beams in [1, 2, 3]

        self.beams = beams
        self.left_beamed = left_beamed
        self.right_beamed = right_beamed

        # computed by the beam instance
        self.left_beam_count = 0
        self.right_beam_count = 0

        # reference to a beam instance set by the canvas when creating the beam
        self.beam = None

    def get_note_generic_annotation(self) -> str:
        SYMBOLS = {
            1: "e",
            2: "s",
            3: "t"
        }
        token = SYMBOLS[self.beams]
        if self.left_beamed:
            token = "=" + token
        if self.right_beamed:
            token += "="
        return token

    def select_sprites(self, mc: Mashcima):
        super().select_sprites(mc)

        # override flip -> pull it from the beam
        self.flipped = self.beam.flipped

    def update_sprites_for_stem_length(self, stem_length: int):
        if not self.sprites.has_sprite("stem"):
            # synthetic images have sprites combined
            self.update_sprites_for_stem_length_combined_image(stem_length)
            return
        
        self.sprites = copy.deepcopy(self.sprites)

        sign = -1 if self.flipped else 1

        stem = self.sprites.sprite("stem")
        lengthen = stem_length + stem.y
        if self.flipped:
            lengthen = stem_length - stem.y - stem.height
        if stem.height + lengthen < 1:
            lengthen = 1 - stem.height
            # Silence this warning because it happens quite often.
            # And the reason is that some notes have stems starting quite
            # far away from the notehead, therefore the scaled height
            # would be negative.
            # print("Stem length for beamed note clamped to minimal height.")
        stem.stretch_height(stem.height + lengthen)

        if not self.flipped:
            stem.y -= lengthen

        sh = self.sprites.point("stem_head")
        sh = (sh[0], sh[1] - sign * lengthen)
        self.sprites.add_point("stem_head", sh)

        self.sprites.recalculate_bounding_box()
    
    def update_sprites_for_stem_length_combined_image(self, target_stem_length: int):
        """
            Performs sprite stretching for combined images (e.g. synthetic images)
            target_stem_length = vertical (y) distance between the sprite group origin
            and the beam line, over the sprite group origin (x)
        """
        self.sprites = copy.deepcopy(self.sprites)
        img = self.sprites.sprite("combined_image")
        
        stem_head_x, stem_head_y = self.sprites.point("stem_head")
        sign = -1 if self.flipped else 1

        current_length = -stem_head_y * sign
        grow_pixels = target_stem_length - current_length
        scale_coef = (current_length + grow_pixels) / current_length

        img.stretch_height(int(img.height * scale_coef))
        img.y = int(img.y * scale_coef)
        
        new_stem_head = (stem_head_x, int(stem_head_y * scale_coef))
        self.sprites.add_point("stem_head", new_stem_head)

        self.sprites.recalculate_bounding_box()

    @property
    def global_stem_head(self):
        sh = self.sprites.point("stem_head")
        return self.sprites.position_x + sh[0], self.sprites.position_y + sh[1]
