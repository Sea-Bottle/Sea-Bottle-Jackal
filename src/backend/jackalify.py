"""A wrapper for getting a video with the distortion process from an image."""
import sys

from cv2 import cv2
from seam_carve import seam_carve
from tqdm import tqdm


def jackalify(image_path: str, video_path: str):
    """Apply the seam carving algorithm to the image and get a video with the distortion process.

    :param image_path: The path to the input image.
    :type image_path: str
    :param video_path: The path to the output video.
    :type video_path: str
    """
    image = cv2.imread(image_path)
    image = cv2.resize(
        image,
        (
            image.shape[1] * 512 // max(image.shape[:2]),
            image.shape[0] * 512 // max(image.shape[:2]),
        ),
    )
    height, width, _ = image.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_path, fourcc, 60, (width, height))

    for _ in tqdm(range(int(min(height, width) * 0.75))):
        image = seam_carve(image, 'horizontal')
        image = seam_carve(image, 'vertical')
        video.write(cv2.resize(image, (width, height)))

    video.release()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise RuntimeError(
            'Usage – python3 jackalify.py input_image_path output_video_path',
        )

    jackalify(sys.argv[1], sys.argv[2])
