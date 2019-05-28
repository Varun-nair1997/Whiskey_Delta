import numpy as np
import scipy as sp
import cv2
import matplotlib as plt
import pywt
import skimage

img = cv2.imread("DSC4.JPG",0)
imgA = np.asarray(img)

#Adding Noise
row,col= imgA.shape #ch
mean = 0
var = 0.1
sigma = var**0.5
gauss = np.random.normal(mean,sigma,(row,col))#ch
gauss = gauss.reshape(row,col)#ch
noisy = imgA + gauss


#print(type(imgA))
#print("imgA=", imgA)
print(noisy.shape)

wavelet = pywt.Wavelet('sym2')
coeffs = pywt.dwt2(noisy, mode='constant',wavelet=wavelet)
LL, (LH, HL, HH) = coeffs #cA:LL cV:LH cD:HH cH: HL.
coeffsA = np.asarray(coeffs)
#avg1 = np.average(imgA)
#print(avg1)

#VISUshrink
TLL = np.sqrt((np.std(LL)**2)*(np.log(1428*2148)))
THH = np.sqrt((np.std(HH)**2)*(np.log(1428*2148)))

tscale =1/2
LL1 =pywt.threshold(LL, TLL*tscale, 'soft')
# pywt.threshold(LH, 150, 'soft', substitute=0)
# pywt.threshold(HL, 150, 'soft', substitute=0)
HH1 = pywt.threshold(HH, THH*tscale, 'soft')
inv = pywt.idwt(LL1, HH1, wavelet=wavelet)
HHscaled = cv2.resize(HH1, (4288,1248))
LLscaled = cv2.resize(LL1, (4288,1248))
invscaled = cv2.resize(inv, (4288,1248))
imgscaled = cv2.resize(noisy, (4288,1248))
# LLflat = np.ravel(LLscaled)
# HHflat = np.ravel(HHscaled)


filter1=cv2.blur(invscaled,(5,5))

#filtered = skimage.filters.wiener(inv,HH1)

print("LL",LL1.shape)
print("HH",HH1.shape)
print(inv.shape)


# cv2.imshow("noisy",(noisy))
# cv2.waitKey()
#
# cv2.imshow("denoised1",(inv))
# cv2.waitKey()
#
# cv2.imshow("inter",(HHscaled))
# cv2.waitKey()
#
cv2.imshow("invscal",(invscaled))
cv2.waitKey()

cv2.imshow("inter",(filter1))
cv2.waitKey()

#filtered = inv+HH

cv2.imshow("orignal",(imgscaled))
cv2.waitKey()

"""
print(type.coeffs)
print("image shape",imgA.shape)
print("cA shape:",cA.shape)
print("cD shape", cD.shape)
"""