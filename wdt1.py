import numpy as np
import scipy as sp
import cv2
import matplotlib as plt
import pywt
import skimage

img = cv2.imread("DSC4.JPG",0)
imgA = np.asarray(img)
# imgC = cv2.equalizeHist(imgB)
# imgA = np.stack((imgB,imgB))
#Adding Noise
row,col = imgA.shape #ch
mean = 0
var = 0.5
sigma = var**0.5
gauss = np.random.normal(mean,sigma,(row,col))#ch
gauss = gauss.reshape(row,col)#ch
noisy = imgA + gauss


#print(type(imgA))
#print("imgA=", imgA)
print(noisy.shape)

wavelet = pywt.Wavelet('haar')
coeffs = pywt.dwt2(noisy, mode='constant',wavelet=wavelet)
LL, (LH, HL, HH) = coeffs #cA:LL cV:LH cD:HH cH: HL.
coeffsA = np.asarray(coeffs)
#avg1 = np.average(imgA)
#print(avg1)

sizeLL = LL.shape
number= sizeLL[0]*sizeLL[1]
sizeimg = imgA.shape
simgx=sizeimg[0]
simgy=sizeimg[1]
#VISUshrink
TLL = np.sqrt((np.std(LL)**2)*(np.log(number)))
THH = np.sqrt((np.std(HH)**2)*(np.log(number)))

tscale = 5/8
LL1 =pywt.threshold(LL, TLL*tscale, 'soft')
# pywt.threshold(LH, 150, 'soft', substitute=0)
# pywt.threshold(HL, 150, 'soft', substitute=0)
HH1 = pywt.threshold(HH, THH*tscale, 'soft')
inv = pywt.idwt(LL1, HH1, wavelet=wavelet)
HHscaled = cv2.resize(HH1, (simgy,simgx))
LLscaled = cv2.resize(LL1, (simgy,simgx))
invscaled = cv2.resize(inv, (simgy,simgx))
imgscaled = cv2.resize(noisy, (simgy,simgx))
# LLflat = np.ravel(LLscaled)
# HHflat = np.ravel(HHscaled)

filter1=cv2.blur(invscaled,(5,5))
filtered = cv2.imwrite('filter1.jpg',filter1)
imgb = cv2.imread('filtered.jpg',0)
imgB = np.asarray(imgb)

#x = cv2.inpaint(imgA, imgB, 3, cv2.INPAINT_NS)

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

print(imgB)

cv2.imshow("invscal",(invscaled))
cv2.waitKey()

cv2.imshow("inter",(filter1))
cv2.waitKey()

cv2.imshow("orignal",(imgscaled))
cv2.waitKey()

# cv2.imshow("psuedo final",(imgB))
# cv2.waitKey()

"""
print(type.coeffs)
print("image shape",imgA.shape)
print("cA shape:",cA.shape)
print("cD shape", cD.shape)
"""