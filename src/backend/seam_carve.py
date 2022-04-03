"""Реализация алгоритма seam carving."""
from typing import Tuple

import numpy as np


def horizontal_shrink(
        image: np.ndarray, derivative: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Горизонтальное сжатие изображения."""
    return shrink(image, derivative)


def vertical_shrink(
        image: np.ndarray, derivative: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Вертикальное сжатие изображения."""
    image, seam = shrink(
        np.transpose(image, axes=(1, 0, 2)), np.transpose(derivative),
    )
    return np.transpose(image, axes=(1, 0, 2)), np.transpose(seam)


def compute_seam(derivative: np.ndarray) -> np.ndarray:
    """Вычисление шва с наименьшей энергией."""
    energy = np.zeros(derivative.shape)
    energy[0] = derivative[0]

    for height in range(1, energy.shape[0]):
        for width in range(energy.shape[1]):
            if width not in (0, energy.shape[1] - 1):
                energy[height, width] = (
                    min(
                        energy[height - 1, width - 1],
                        energy[height - 1, width],
                        energy[height - 1, width + 1],
                    ) + derivative[height, width]
                )
            elif width != 0 and width == energy.shape[1] - 1:
                energy[height, width] = (
                    min(
                        energy[height - 1, width - 1],
                        energy[height - 1, width],
                    ) + derivative[height, width]
                )
            elif width == 0 and width != energy.shape[1] - 1:
                energy[height, width] = (
                    min(
                        energy[height - 1, width],
                        energy[height - 1, width + 1],
                    ) + derivative[height, width]
                )
            else:
                energy[height, width] = (
                    energy[height - 1, width] + derivative[height, width]
                )

    seam = np.zeros(energy.shape)
    index = np.argmin(energy[-1])

    seam[-1, index] = True

    for height in range(energy.shape[0] - 2, -1, -1):
        if index not in (0, energy.shape[1] - 1):
            index += np.argmin(energy[height, index - 1: index + 2]) - 1
        elif index != 0 and index == energy.shape[1] - 1:
            index += np.argmin(energy[height, index - 1: index + 1]) - 1
        elif index == 0 and index != energy.shape[1] - 1:
            index += np.argmin(energy[height, index: index + 2])

        seam[height, index] = True

    return seam


def shrink(
        image: np.ndarray, derivative: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Сжатие изображения."""
    seam = compute_seam(derivative)

    red = np.ma.compressed(np.ma.MaskedArray(image[:, :, 0], mask=seam))
    green = np.ma.compressed(np.ma.MaskedArray(image[:, :, 1], mask=seam))
    blue = np.ma.compressed(np.ma.MaskedArray(image[:, :, 2], mask=seam))

    red = red.reshape(image.shape[0], image.shape[1] - 1)
    green = green.reshape(image.shape[0], image.shape[1] - 1)
    blue = blue.reshape(image.shape[0], image.shape[1] - 1)

    image = np.dstack((red, green, blue))

    return image, seam


FUNCTIONS = {
    'horizontal shrink': horizontal_shrink,
    'vertical shrink': vertical_shrink,
}


def seam_carve(
        image: np.ndarray, action: str,
) -> Tuple[np.ndarray, np.ndarray]:
    """Основная функция алгоритма seam carving."""
    brightness = (
        image[:, :, 0] * 0.299 + image[:, :, 1] * 0.587 + image[:, :, 2] * 0.114
    )

    append_up = np.append(brightness[0][np.newaxis], brightness, axis=0)[:-1]
    append_down = np.append(brightness, brightness[-1][np.newaxis], axis=0)[1:]

    append_left = np.append(
        brightness[:, 0][:, np.newaxis], brightness, axis=1,
    )[:, :-1]
    append_right = np.append(
        brightness, brightness[:, -1][:, np.newaxis], axis=1,
    )[:, 1:]

    derivative_x = append_right - append_left
    derivative_y = append_down - append_up
    derivative = np.sqrt(derivative_x ** 2 + derivative_y ** 2)

    return FUNCTIONS[action](image, derivative)
