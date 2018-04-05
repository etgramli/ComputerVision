import numpy as np
import math


def affine_transform(A, a, img, bilinear=False):
    """
    Defines an affine transformation of an image.
    :param A: Matrix
    :param a: Verschiebungsvektor
    :param img: Eingabebild
    :param bilinear: Toggle for using bilinear interpolation
    :return: Affin verzerrtes Eingabebild
    """
    orig_shape = img.shape
    if len(orig_shape) == 3:
        new_shape = tuple([int(orig_shape[0] + orig_shape[0] * 0.1),
                           int(orig_shape[1] + orig_shape[1] * 0.1),
                           orig_shape[2]])
    else:
        new_shape = tuple([int(orig_shape[0] + orig_shape[0] * 0.1),
                           int(orig_shape[1] + orig_shape[1] * 0.1)])
    new_img = np.zeros(new_shape, img.dtype)

    for x in range(0, new_img.shape[0]):
        for y in range(0, new_img.shape[1]):
            new_coprdinates = np.array([x, y])
            original_coordinates = np.subtract(np.dot(np.linalg.inv(A), new_coprdinates), a)
            if original_coordinates[0] < orig_shape[0] and original_coordinates[1] < orig_shape[1]:
                if bilinear:
                    new_img[x][y] = bilinear_interpolation(img, original_coordinates[0], original_coordinates[1])
                else:
                    new_img[x][y] = img[int(original_coordinates[0])][int(original_coordinates[1])]
    return new_img


def bilinear_interpolation(img, x, y):
    """
    Produces an interpolated (bilinear) version of img of size A.
    :param img: Source image.
    :param x: x coordinate of the source image to fetch (float)
    :param y: y coordinate of the source image to fetch (float)
    :return: Bilinear interpolateion of (x/y)
    """
    a1 = (x - math.floor(x)) * (y - math.floor(y))
    a2 = (x - math.floor(x)) * (math.ceil(y) - y)
    a3 = (math.ceil(x) - x) * (y - math.floor(y))
    a4 = (math.ceil(x) - x) * (math.ceil(y) - y)
    weighted_sum = a1 * get_with_default(img, math.ceil(x), math.ceil(y)) +\
                   a2 * get_with_default(img, math.ceil(x), math.floor(y)) +\
                   a3 * get_with_default(img, math.floor(x), math.ceil(y)) +\
                   a4 * get_with_default(img, math.floor(x), math.floor(y))
    return weighted_sum


def get_with_default(img, x, y, default=0):
    """
    Returns the value of the matrix at the given point or the default value if it is out of bounds.
    :param img: ndarray
    :param x: X coordinate
    :param y: Y coordinate
    :param default: The default value to be retuned if coordinates are out of bound.
    :return: Type of matrix or default value.
    """
    if x >= img.shape[0] or y >= img.shape[1]:
        return default
    else:
        return img[x][y]


def normalize_color(pixel_array):
    max = get_max(pixel_array)
    if max == 0:
        return pixel_array
    factor = 255 / max
    normalized = tuple([
        np.uint8(pixel_array[0] / factor),
        np.uint8(pixel_array[1] / factor),
        np.uint8(pixel_array[2] / factor)
    ])
    return normalized


def get_max(pixel_array):
    max = 0
    if pixel_array[0] > max:
        max = pixel_array[0]
    if pixel_array[1] > max:
        max = pixel_array[1]
    if pixel_array[2] > max:
        max = pixel_array[2]
    return max