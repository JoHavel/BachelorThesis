import numpy as np
from typing import List, Callable
from app.Dataset import Dataset


class AnnotationsDataset(Dataset):
    """
    Contains a list of mashcima annotations
    and lazily generates corresponding images
    """

    def __init__(
            self,
            annotations: List[str],
            generator: Callable[[int, List[str]], np.ndarray]
    ):
        super().__init__()

        # list of annotations representing the data
        self.annotations = annotations

        # generator that turns annotations to images
        # (gets annotation index and list of all annotations)
        self.generator = generator

    #############
    # Debugging #
    #############

    def check_dataset_visually(self, example_count=10, quiet=False, directory="tf-logs/visual-check"):
        """Shows couple of items in the dataset to visually check the content"""
        import random
        if quiet:
            import os
            import cv2
            os.makedirs(directory, exist_ok=True)
        else:
            import matplotlib.pyplot as plt

        for i in range(example_count):
            index = random.randint(0, self.size - 1)
            print("[" + str(i) + "]", self.get_annotation(index))
            if quiet:
                img = (1.0 - self.get_image(index)) * 255
                img = img.astype(np.uint8)
                cv2.imwrite(
                    os.path.join(directory, str(i).zfill(3) + ".png"),
                    np.dstack([img, img, img])
                )
            else:
                plt.imshow(self.get_image(index))
                plt.show()

    ###########################
    # Internal data interface #
    ###########################

    @property
    def size(self) -> int:
        return len(self.annotations)

    def get_annotation(self, index: int) -> str:
        return self.annotations[index]

    def get_image(self, index: int) -> np.ndarray:
        return self.generator(index, self.annotations)
