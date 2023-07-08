import os
import cv2
from typing import List

from mashcima import Mashcima
from mashcima.Sprite import Sprite

_PATH = os.path.join(os.path.dirname(__file__), "generated_symbols")


def _load_sprite(directory: str, index: int) -> Sprite:
    """
        Loads one Sprite from png and txt file
        Modified :func:`._load_default_sprite`
    """
    img_path = os.path.join(directory, f"im{index}.png")
    center_path = os.path.join(directory, f"im{index}.txt")
    if not os.path.isfile(img_path):
        raise Exception(f"Out of images or bad image names (should be im0.png, im1.png, ...) in directory `{directory}` with index {index}.")
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
    directory = os.path.join(_PATH, dir_name)
    if not os.path.isdir(directory):
        raise Exception("Cannot load sprite directory: " + dir_name)
    sprites: List[Sprite] = []
    for i in range(n):
        sprites.append(_load_sprite(directory, i))
    return sprites


def apply_fraction(
        self: Mashcima,
        muscima_fraction: float,
        generated_fraction: float,
):
    """
        Leaves `muscima_fraction` of original symbols in Mashcima
        and ads `generated_fraction` * len(original symbols) of new symbols from `_PATH`
    """
    sharps_len = len(self.SHARPS)
    self.SHARPS = self.SHARPS[:int(sharps_len * muscima_fraction)] + _load_sprites("sharp", int(sharps_len * generated_fraction))
    flats_len = len(self.FLATS)
    self.FLATS = self.FLATS[:int(flats_len * muscima_fraction)] + _load_sprites("flat", int(flats_len * generated_fraction))
    naturals_len = len(self.NATURALS)
    self.NATURALS = self.NATURALS[:int(naturals_len * muscima_fraction)] + _load_sprites("natural", int(naturals_len * generated_fraction))
