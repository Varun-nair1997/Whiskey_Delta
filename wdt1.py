import numpy as np
import scipy as sp
import cv2
import matplotlib as plt
import pywt

img = cv2.imread("DSC1.jpeg", 0)
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

wavelet = pywt.Wavelet('db5')
coeffs = pywt.dwt2(noisy, mode='constant',wavelet=wavelet)
LL, (LH, HL, HH) = coeffs #cA:LL cV:LH cD:HH cH: HL.
coeffsA = np.asarray(coeffs)
#avg1 = np.average(imgA)
#print(avg1)

#VISUshrink
TLL = np.sqrt((np.std(LL)**2)*(np.log(1428*2148)))
THH = np.sqrt((np.std(HH)**2)*(np.log(1428*2148)))

LL1 =pywt.threshold(LL, TLL/2, 'soft')
# pywt.threshold(LH, 150, 'soft', substitute=0)
# pywt.threshold(HL, 150, 'soft', substitute=0)
HH1 = pywt.threshold(HH, THH/2, 'soft')


inv = pywt.idwt(LL1, HH1, 'db5')

print("LL",LL1.shape)
print("HH",HH1.shape)
print(inv.shape)


cv2.imshow("noisy",(noisy))
cv2.waitKey()

cv2.imshow("denoised1",(inv))
cv2.waitKey()

"""
cv2.imshow("denoised3",(inv))
cv2.waitKey()


print("cA =", cA)
print("cV =", cV)
print(coeffsA)

print(type.coeffs)
print("image shape",imgA.shape)
print("cA shape:",cA.shape)
print("cD shape", cD.shape)
"""