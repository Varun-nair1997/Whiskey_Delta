import numpy as np
import scipy as sp
import cv2
import matplotlib as plt
import pywt

img = cv2.imread("DSC1.jpeg", 0)
imgA = np.asarray(img)


#print(type(imgA))
#print(imgA)
coeffs = pywt.dwt2(imgA, 'haar')
cA, (cH, cV, cD) = coeffs #cA:          cV:         cD:         cH:         .
coeffsA = np.asarray(coeffs)

print("cA =", cA)
print("cV =", cV)
print(coeffsA)

print(type.coeffs)
print("image shape",imgA.shape)
print("cA shape:",cA.shape)
print("cD shape", cD.shape)
