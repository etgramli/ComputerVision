from skimage import data, io, color
from matplotlib import pyplot as plt
import numpy as np
import UebungEins.AffineTransform


rotate = np.array([[0.866, -0.5],
                   [0.5, 0.866]])
scale = np.array([[0.7, 0],
                  [0, 0.7]])
transform = np.array([[0.8, 0],
                      [0, 1.2]])
dehnen = "Dehnen um 1,5 entlang der Diagonalen, stauchen 0,5 senkrecht dazu"
entzerr = np.array([[0.891, -0.454],
                    [0.454, 0.891]])

vector = np.array([0, 0])


gletscher = data.imread("resources/gletscher.jpg")
ambassadors = data.imread("resources/ambassadors.jpg")
schraegbild_tempelhof = data.imread("resources/schraegbild_tempelhof.jpg")

gletscher = color.rgb2gray(gletscher)

img1 = UebungEins.AffineTransform.affine_transform(A=rotate, a=vector, img=gletscher, bilinear=True)


io.imshow(img1)
plt.show()
