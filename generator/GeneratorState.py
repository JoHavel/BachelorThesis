import numpy as np
from typing import List, Dict


class GeneratorState:
    """Represents state of the generator at some point
    in time during generation"""
    def __init__(self):
        # generated staff image
        self.img: np.ndarray = None

        # mapping from note position to pixel position
        self.note_positions: Dict[int, int] = {}

        # label for the generated data item
        self.annotation: List[str] = []

        # printer head position in pixels (what has already been printed)
        self.head = 0

        from generator.generate_staff_lines import generate_staff_lines
        self.img, self.note_positions = generate_staff_lines()
