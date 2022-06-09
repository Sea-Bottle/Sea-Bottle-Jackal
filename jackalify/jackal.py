"""A wrapper for getting a video with the distortion process from an image."""
import gettext
import io
import os
import sys
from typing import Optional

import numpy as np
from PIL import Image
import cv2
from tqdm import tqdm

from jackalify.seam_carve import seam_carve  # noqa

project_dir = os.path.dirname(__file__)
translation = gettext.translation('jackalify', localedir=os.path.join(project_dir, 'locales'), languages=['en', 'ru'])
_ = translation.gettext

it = 0
max_it = 0


def jackalify(in_image_path: str, video_path: Optional[str] = None, out_image_path: Optional[str] = None):
    """Apply the seam carving algorithm to the image and get a video with the distortion process.

    :param in_image_path: The path to the input image.
    :type in_image_path: str
    :param video_path: The path to the output video (if None then no video would be generated).
    :type video_path: str
    :param out_image_path: The path to the output image (if None then no photo would be generated).
    :type out_image_path: str
    """
    global it
    global max_it

    if not video_path and not out_image_path:
        raise AttributeError("At least one of output paths should be defined!")

    image = cv2.cv2.cvtColor(cv2.cv2.imread(in_image_path), cv2.cv2.COLOR_BGR2RGB)
    image = cv2.cv2.resize(
        image,
        (
            image.shape[1] * 512 // max(image.shape[:2]),
            image.shape[0] * 512 // max(image.shape[:2]),
        ),
    )

    height, width, _ = image.shape

    frames = []

    max_it = int(min(height, width) * 0.75)
    for it in tqdm(range(max_it)):
        image = seam_carve(image, 'horizontal')
        image = seam_carve(image, 'vertical')
        frames.append(Image.fromarray(np.uint8(cv2.resize(image, (width, height))), mode="RGB"))

    if out_image_path:
        frames[-1].save(out_image_path)

    if video_path:
        animated_gif = io.BytesIO()
        frames[0].save(
            animated_gif,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=25,
            loop=0
        )
        animated_gif.seek(0)
        with open(video_path, 'wb') as gif_file:
            gif_file.write(animated_gif.read())


def getProgress():
    """Get progress of jackalify."""
    global it
    global max_it
    return (it * 100 // max_it) if max_it > 0 else 0


def main():
    """Run the main function."""
    message = _('Usage – python jackalify.py input_image_path output_video_path')
    if len(sys.argv) != 3:
        raise RuntimeError(message)

    jackalify(sys.argv[1], sys.argv[2])
