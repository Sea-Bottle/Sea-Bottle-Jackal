"""Обертка для получения видео с процессом искажения из изображения."""
import sys

from cv2 import cv2
from seam_carve import seam_carve
from tqdm import tqdm


def jackalify(image_path: str, video_path: str):
    """Применить алгоритм seam carving к изображению и получить видео с процессом искажения."""
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
        image = seam_carve(image, 'horizontal shrink')[0]
        image = seam_carve(image, 'vertical shrink')[0]
        video.write(cv2.resize(image, (width, height)))

    video.release()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise RuntimeError(
            'Usage – python3 jackalify.py input_image_path output_video_path',
        )

    jackalify(sys.argv[1], sys.argv[2])
