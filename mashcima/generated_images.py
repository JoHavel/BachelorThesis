import os
import cv2
from typing import List

from mashcima import Mashcima
from mashcima.Sprite import Sprite
from mashcima.SpriteGroup import SpriteGroup
import config


def _load_sprite(directory: str, index: int) -> Sprite:
    """
        Loads one Sprite from png and txt file
        Modified :func:`._load_default_sprite`
    """
    img_path = os.path.join(directory, f"im{index}.png")
    center_path = os.path.join(directory, f"im{index}.txt")
    if not os.path.isfile(img_path):
        raise Exception(
            f"Out of images or bad image names (should be im0.png, " + \
            f"im1.png, ...) in directory `{directory}` with index {index}."
        )
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) / 255
    x = -img.shape[1] // 2
    y = -img.shape[0] // 2
    if os.path.isfile(center_path):
        with open(center_path) as f:
            x, y = tuple(f.readline().split())
            x = -int(x)
            y = -int(y)
    return Sprite(x, y, img)


def _load_sprites(dir_name: str, n: int) -> List[Sprite]:
    """
        Loads `n` sprites from directory `dir_name`
    """
    directory = os.path.join(config.SYNTHETIC_SYMBOLS_PATH, dir_name)
    if not os.path.isdir(directory):
        raise Exception("Cannot load sprite directory: " + dir_name)
    sprites: List[Sprite] = []
    for i in range(n):
        sprites.append(_load_sprite(directory, i))
    print(f"Loaded {len(sprites)} synthetic images: {dir_name}")
    return sprites


def _load_stemmed_note(directory: str, index: int) -> SpriteGroup:
    """
        Loads one 'stemmed note' SpriteGroup from one png and two txt files
    """
    img_path = os.path.join(directory, f"im{index}.png")
    origin_path = os.path.join(directory, f"im{index}-origin.txt")
    stem_head_path = os.path.join(directory, f"im{index}-stem_head.txt")
    if not os.path.isfile(img_path):
        raise Exception(
            f"Out of images or bad image names (should be im0.png, " + \
            f"im1.png, ...) in directory `{directory}` with index {index}."
        )
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) / 255
    with open(origin_path) as f:
        origin_x, origin_y = tuple(int(coord) for coord in f.readline().split())
    with open(stem_head_path) as f:
        stem_head_x, stem_head_y = tuple(int(coord) for coord in f.readline().split())

    sprite_group = SpriteGroup()
    sprite_group.add("combined_image", Sprite(-origin_x, -origin_y, img))
    sprite_group.add_point(
        "stem_head", (stem_head_x - origin_x, stem_head_y - origin_y)
    )
    return sprite_group


def _load_stemmed_notes(dir_name: str, n: int) -> List[SpriteGroup]:
    """
        Loads `n` sprite groups containing a note with 
        a stem from directory `dir_name`
    """
    directory = os.path.join(config.SYNTHETIC_SYMBOLS_PATH, dir_name)
    if not os.path.isdir(directory):
        raise Exception("Cannot load sprite directory: " + dir_name)
    sprite_groups: List[SpriteGroup] = []
    for i in range(n):
        sprite_groups.append(_load_stemmed_note(directory, i))
    print(f"Loaded {len(sprite_groups)} synthetic images: {dir_name}")
    return sprite_groups


def _load_sprite_groups(dir_name: str, n: int, point_name: str) -> List[SpriteGroup]:
    """Loads sprite groups that contain only a single sprite"""
    sprites = _load_sprites(dir_name=dir_name, n=n)
    sprite_groups: List[SpriteGroup] = []
    for sprite in sprites:
        group = SpriteGroup()
        group.add(point_name, sprite)
        sprite_groups.append(group)
    return sprite_groups


def apply_fraction(
        self: Mashcima,
        muscima_fraction: float,
        generated_fraction: float,
):
    """
        Leaves `muscima_fraction` of original symbols in Mashcima
        and ads `generated_fraction` * len(original symbols) of new symbols
        from `config.SYNTHETIC_SYMBOLS_PATH`
    """

    # stemmed notes
    half_notes_len = len(self.HALF_NOTES)
    self.HALF_NOTES = self.HALF_NOTES[:int(half_notes_len * muscima_fraction)] \
        + _load_stemmed_notes("half-note", int(half_notes_len * generated_fraction))
    quarter_notes_len = len(self.QUARTER_NOTES)
    self.QUARTER_NOTES = self.QUARTER_NOTES[:int(quarter_notes_len * muscima_fraction)] \
        + _load_stemmed_notes("quarter-note", int(quarter_notes_len * generated_fraction))
    eighth_notes_len = len(self.EIGHTH_NOTES)
    self.EIGHTH_NOTES = self.EIGHTH_NOTES[:int(eighth_notes_len * muscima_fraction)] \
        + _load_stemmed_notes("eighth-note", int(eighth_notes_len * generated_fraction))
    sixteenth_notes_len = len(self.SIXTEENTH_NOTES)
    self.SIXTEENTH_NOTES = self.SIXTEENTH_NOTES[:int(sixteenth_notes_len * muscima_fraction)] \
        + _load_stemmed_notes("sixteenth-note", int(sixteenth_notes_len * generated_fraction))

    # sprite-only symbols
    sharps_len = len(self.SHARPS)
    self.SHARPS = self.SHARPS[:int(sharps_len * muscima_fraction)] \
        + _load_sprites("sharp", int(sharps_len * generated_fraction))
    flats_len = len(self.FLATS)
    self.FLATS = self.FLATS[:int(flats_len * muscima_fraction)] \
        + _load_sprites("flat", int(flats_len * generated_fraction))
    naturals_len = len(self.NATURALS)
    self.NATURALS = self.NATURALS[:int(naturals_len * muscima_fraction)] \
        + _load_sprites("natural", int(naturals_len * generated_fraction))

    # TODO: sprite-group items with only one sprite
    # whole_notes_len = len(self.WHOLE_NOTES)
    # self.WHOLE_NOTES = self.WHOLE_NOTES[:int(whole_notes_len * muscima_fraction)] \
    #     + _load_sprite_groups( "whole-note", int(whole_notes_len * generated_fraction),
    #         "notehead")
