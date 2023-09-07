import os
import cv2
import shutil
import copy
import numpy as np
from typing import List, Dict
from mashcima import Mashcima
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup


mc = Mashcima(use_cache=True, skip_writers=[13, 17, 20, 34, 41, 49])
export_path = "datasets/muscima-exported-symbols"


def export_sprite_group(
    dir_name: str,
    sprite_groups: List[SpriteGroup],
    export_points: Dict[str, str] = {}
):
    dir_path = os.path.join(export_path, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    for i, sprite_group in enumerate(sprite_groups):
        img = sprite_group.inspect(draw_origin=False, draw_points=False)
        img_path = os.path.join(dir_path, f"im{i}.png")
        cv2.imwrite(img_path, img * 255)

        origin_path = os.path.join(dir_path, f"im{i}.txt")
        with open(origin_path, "w") as f:
            notehead = (str(-sprite_group.left), str(-sprite_group.top))
            f.write(" ".join(notehead))
        
        for point_name, suffix in export_points.items():
            point_path = os.path.join(dir_path, f"im{i}-{suffix}.txt")
            point_x, point_y = sprite_group.point(point_name)
            with open(point_path, "w") as f:
                transformed_point = (
                    str(-sprite_group.left + point_x),
                    str(-sprite_group.top + point_y)
                )
                f.write(" ".join(transformed_point))


def export_sprite(dir_name: str, sprites: List[Sprite]):
    export_sprite_group(
        dir_name,
        [SpriteGroup().add("_", s) for s in sprites]
    )


def flip_flags(sprite_groups: List[SpriteGroup]):
    sprite_groups = copy.deepcopy(sprite_groups)
    for group in sprite_groups:
        if group.has_sprite("flag_8"):
            f = group.sprite("flag_8")
            f.mask = np.flip(f.mask, axis=1)
            f.x -= f.width
        if group.has_sprite("flag_16"):
            f = group.sprite("flag_16")
            f.mask = np.flip(f.mask, axis=1)
            f.x -= f.width
    return sprite_groups


########
# MAIN #
########

print("Clearing the export folder...")
shutil.rmtree(export_path)

print("Exporting...")

export_sprite("sharp", mc.SHARPS)
export_sprite("flat", mc.FLATS)
export_sprite("natural", mc.NATURALS)

export_sprite_group("whole-note", mc.WHOLE_NOTES)
export_sprite_group("quarter-rest", mc.QUARTER_RESTS)
export_sprite_group("c-clef", mc.C_CLEFS)
export_sprite_group("g-clef", mc.G_CLEFS)
export_sprite_group("f-clef", mc.F_CLEFS)

export_sprite_group("half-note", mc.HALF_NOTES, { "stem_head": "stem_head" })
export_sprite_group("quarter-note", mc.QUARTER_NOTES, { "stem_head": "stem_head" })

export_sprite_group("eighth-note-up", mc.EIGHTH_NOTES, { "stem_head": "stem_head" })
export_sprite_group("eighth-note-down", flip_flags(mc.EIGHTH_NOTES), { "stem_head": "stem_head" })

print("Done.")
