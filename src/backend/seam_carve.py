from typing import Optional
from typing import Tuple

import numpy as np


def horizontal_shrink(
        image: np.ndarray, derivative: np.ndarray, mask: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    return shrink(image, derivative, mask)


def vertical_shrink(
        image: np.ndarray, derivative: np.ndarray, mask: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    image, mask, seam = shrink(
        np.transpose(image, axes=(1, 0, 2)),
        np.transpose(derivative),
        np.transpose(mask),
    )
    return (
        np.transpose(image, axes=(1, 0, 2)),
        np.transpose(mask),
        np.transpose(seam),
    )


def horizontal_expand(
        image: np.ndarray, derivative: np.ndarray, mask: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    return expand(image, derivative, mask)


def vertical_expand(
        image: np.ndarray, derivative: np.ndarray, mask: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    image, mask, seam = expand(
        np.transpose(image, axes=(1, 0, 2)),
        np.transpose(derivative),
        np.transpose(mask),
    )
    return (
        np.transpose(image, axes=(1, 0, 2)),
        np.transpose(mask),
        np.transpose(seam),
    )


def compute_seam(derivative: np.ndarray) -> np.ndarray:
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
                    )
                    + derivative[height, width]
                )
            elif width != 0 and width == energy.shape[1] - 1:
                energy[height, width] = (
                    min(
                        energy[height - 1, width - 1],
                        energy[height - 1, width],
                    )
                    + derivative[height, width]
                )
            elif width == 0 and width != energy.shape[1] - 1:
                energy[height, width] = (
                    min(
                        energy[height - 1, width],
                        energy[height - 1, width + 1],
                    )
                    + derivative[height, width]
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
            index += np.argmin(energy[height, index - 1 : index + 2]) - 1
        elif index != 0 and index == energy.shape[1] - 1:
            index += np.argmin(energy[height, index - 1 : index + 1]) - 1
        elif index == 0 and index != energy.shape[1] - 1:
            index += np.argmin(energy[height, index : index + 2])

        seam[height, index] = True

    return seam


def shrink(
        image: np.ndarray, derivative: np.ndarray, mask: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    seam = compute_seam(derivative)

    red = np.ma.compressed(np.ma.MaskedArray(image[:, :, 0], mask=seam))
    green = np.ma.compressed(np.ma.MaskedArray(image[:, :, 1], mask=seam))
    blue = np.ma.compressed(np.ma.MaskedArray(image[:, :, 2], mask=seam))
    mask = np.ma.compressed(np.ma.MaskedArray(mask, mask=seam))

    red = red.reshape(image.shape[0], image.shape[1] - 1)
    green = green.reshape(image.shape[0], image.shape[1] - 1)
    blue = blue.reshape(image.shape[0], image.shape[1] - 1)
    mask = mask.reshape(image.shape[0], image.shape[1] - 1)

    image = np.dstack((red, green, blue))

    return image, mask, seam


def expand(
        image: np.ndarray, derivative: np.ndarray, mask: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    seam = compute_seam(derivative)

    red = np.zeros((image.shape[0], image.shape[1] + 1))
    green = np.zeros((image.shape[0], image.shape[1] + 1))
    blue = np.zeros((image.shape[0], image.shape[1] + 1))
    expanded_mask = np.zeros((image.shape[0], image.shape[1] + 1))

    for height in range(image.shape[0]):
        index = np.argmax(seam[height])

        red[height, : index + 1] = image[height, : index + 1, 0]
        red[height, index + 2 :] = image[height, index + 1 :, 0]
        red[height, index + 1] = red[height, index]

        green[height, : index + 1] = image[height, : index + 1, 1]
        green[height, index + 2 :] = image[height, index + 1 :, 1]
        green[height, index + 1] = green[height, index]

        blue[height, : index + 1] = image[height, : index + 1, 2]
        blue[height, index + 2 :] = image[height, index + 1 :, 2]
        blue[height, index + 1] = blue[height, index]

        expanded_mask[height, : index + 1] = mask[height, : index + 1]
        expanded_mask[height, index + 2 :] = mask[height, index + 1 :]
        expanded_mask[height, index + 1] = expanded_mask[height, index]

    image = np.dstack((red, green, blue))

    return image, expanded_mask, seam


FUNCTIONS = {
    'horizontal shrink': horizontal_shrink,
    'vertical shrink': vertical_shrink,
    'horizontal expand': horizontal_expand,
    'vertical expand': vertical_expand,
}


def seam_carve(
        image: np.ndarray, action: str, mask: Optional[np.ndarray] = None,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if mask is None:
        mask = np.zeros(image.shape[:-1])

    brightness = (
        image[:, :, 0] * 0.299
        + image[:, :, 1] * 0.587
        + image[:, :, 2] * 0.114
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
    derivative += mask.astype('float64') * mask.shape[0] * mask.shape[1] * 256

    return FUNCTIONS[action](image, derivative, mask)
