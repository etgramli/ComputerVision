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
    new_shape = tuple([int(orig_shape[0] + orig_shape[0] * 0.1),
                       int(orig_shape[1] + orig_shape[1] * 0.1),
                       orig_shape[2]])
    new_img = np.zeros(new_shape, img.dtype)

    for x in range(0, img.shape[0]):
        for y in range(0, img.shape[1]):
            original_coordinates = np.array([x, y])
            new_coprdinates = np.add(np.dot(A, original_coordinates), a)
            if new_coprdinates[0] <= new_shape[0] and new_coprdinates[1] <= new_shape[1]:
                if bilinear:
                    new_img[int(new_coprdinates[0])][int(new_coprdinates[1])] = bilinear_interpolation(img, x, y)
                else:
                    new_img[int(new_coprdinates[0])][int(new_coprdinates[1])] = img[x][y]
    return new_img


def affine_transform_on_new_image(A, a, img, bilinear=False):
    """
    Defines an affine transformation of an image.
    :param A: Matrix
    :param a: Verschiebungsvektor
    :param img: Eingabebild
    :param bilinear: Toggle for using bilinear interpolation
    :return: Affin verzerrtes Eingabebild
    """
    orig_shape = img.shape
    new_shape = tuple([int(orig_shape[0] + orig_shape[0] * 0.1),
                       int(orig_shape[1] + orig_shape[1] * 0.1),
                       orig_shape[2]])
    new_img = np.zeros(new_shape, img.dtype)

    for x in range(0, new_shape[0]):
        for y in range(0, new_shape[1]):
            original_coordinates = np.array([x, y])
            new_coprdinates = np.add(np.dot(A, original_coordinates), a)
            if new_coprdinates[0] <= new_shape[0] and new_coprdinates[1] <= new_shape[1]:
                if bilinear:
                    new_img[int(new_coprdinates[0])][int(new_coprdinates[1])] = bilinear_interpolation(img, x, y)
                else:
                    new_img[int(new_coprdinates[0])][int(new_coprdinates[1])] = img[x][y]
    return new_img


def bilinear_interpolation(img, x, y):
    """
    Produces an interpolated (bilinear) version of img of size A.
    :param img: Source image.
    :param x: x coordinate of the source image to fetch (float)
    :param y: y coordinate of the source image to fetch (float)
    :return: Bilinear interpolateion of (x/y)
    """
    a1 = (math.floor(x) + x) * (math.floor(y) + y)
    a2 = (math.floor(x) + x) * (math.ceil(y) - y)
    a3 = (math.ceil(x) - x) * (math.floor(y) + y)
    a4 = (math.ceil(x) - x) * (math.ceil(y) - y)
    weighted_sum = a1 * img[math.ceil(x)][math.ceil(y)] +\
                   a2 * img[math.ceil(x)][math.floor(y)] +\
                   a3 * img[math.floor(x)][math.ceil(y)] +\
                   a4 * img[math.floor(x)][math.floor(y)]
    return normalize_color(weighted_sum)


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