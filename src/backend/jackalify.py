"""A wrapper for getting a video with the distortion process from an image."""
import gettext
import os
import sys

from cv2 import cv2
from tqdm import tqdm
from PIL import Image
import numpy as np

from seam_carve import seam_carve

translation = gettext.translation('src', localedir=os.path.join(os.environ['PROJECT_ROOT'], 'locales'), languages=['en', 'ru'])
_ = translation.gettext

it = 0
max_it = 0


def jackalify(image_path: str, video_path: str):
    """Apply the seam carving algorithm to the image and get a video with the distortion process.

    :param image_path: The path to the input image.
    :type image_path: str
    :param video_path: The path to the output video.
    :type video_path: str
    """
    global it
    global max_it

    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    image = cv2.resize(
        image,
        (
            image.shape[1] * 512 // max(image.shape[:2]),
            image.shape[0] * 512 // max(image.shape[:2]),
        ),
    )

    height, width, _ = image.shape

    frames = []

    max_it = int(min(height, width) * 0.75)
    it = 0
    for _ in tqdm(range(int(min(height, width) * 0.75))):
        image = seam_carve(image, 'horizontal')
        image = seam_carve(image, 'vertical')
        frames.append(Image.fromarray(np.uint8(cv2.resize(image, (width, height))), mode="RGB"))
        it += 1

    frames[0].save(
        video_path,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=25,
        loop=0
    )


def getProgress():
    """Get progress of jackalify."""
    global it
    global max_it
    return int(it / max_it * 100)


def main():
    """Run the main function."""
    message = _('Usage – python3 jackalify.py input_image_path output_video_path')
    if len(sys.argv) != 3:
        raise RuntimeError(message)

    jackalify(sys.argv[1], sys.argv[2])
