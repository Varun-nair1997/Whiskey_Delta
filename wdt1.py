import numpy as np
import scipy as sp
import cv2
import matplotlib as plt
import pywt
import skimage


img = cv2.imread("DSC1.jpeg",0)
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
#noisy = imgA+gauss


filterdim = imgA.shape
#enhancing brightness
alpha = 1.1
beta = 10
filter2 = np.zeros(filterdim,imgA.dtype)
for y in range(filterdim[0]):
    for x in range(filterdim[1]):
        filter2[y, x] = np.clip(alpha * imgA[y, x] + beta, 0, 255)

noisy = filter2

#print(type(imgA))
#print("imgA=", imgA)
print(noisy.shape)

#wavelet transform
wavelet = pywt.Wavelet('haar')
coeffs = pywt.dwt2(noisy, mode='constant',wavelet=wavelet)
LL, (LH, HL, HH) = coeffs #cA:LL cV:LH cD:HH cH: HL.
coeffsA = np.asarray(coeffs)


sizeLL = imgA.shape
number= sizeLL[0]*sizeLL[1]
sizeimg = imgA.shape
simgx=sizeimg[0]
simgy=sizeimg[1]

#VISUshrink
TLL = np.sqrt((np.std(LL)**2)*(np.log(number)))
THH = np.sqrt((np.std(HH)**2)*(np.log(number)))

tscale = 1/3
LL1 =pywt.threshold(LL, TLL*tscale, 'soft')
HH1 = pywt.threshold(HH, THH*tscale, 'soft')

#inverse transform
inv = pywt.idwt(LL1, HH1, wavelet=wavelet)

#HHscaed = cv2.resize(HH1, (simgy,simgx))
#LLscaled = cv2.resize(LL1, (simgy,simgx))
invscaled = cv2.resize(inv, (simgy,simgx))
#imgscaled = cv2.resize(noisy, (simgy,simgx))

filter1= invscaled #cv2.blur(invscaled,(5,5))

filtered = cv2.imwrite('filter1.jpg',filter1)
imgb = cv2.imread('filter1.jpg',0)
imgB = np.asarray(imgb)
print(filterdim[1])


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


# cv2.imshow("invscal",(invscaled))
# cv2.waitKey()

cv2.imshow("abc",(imgA)) #original
cv2.waitKey()
#
cv2.imshow("xyz",(imgB)) #denoised
cv2.waitKey()

cv2.imshow("pqr",(noisy)) #filter2
cv2.waitKey()

"""
print(type.coeffs)
print("image shape",imgA.shape)
print("cA shape:",cA.shape)
print("cD shape", cD.shape)
"""