import numpy as np
import scipy as sp
import cv2
import matplotlib as mtplib
import pywt as wt

img = cv2.imread("DSC1.jpeg", 0)
imgA = np.asarray(img)

print(imgA.shape)
#print(type(imgA))
#print(imgA)
coeffs = wt.dwt2(imgA, 'haar')
cA, (cH, cV, cD) = coeffs

print(cA)
print(cV)
