import numpy as np
import cv2
import pywt

img = cv2.imread("DSC1.jpeg", 0)
imgA = np.asarray(img) #imgA is the image as an Array
filterdim = imgA.shape #dimensions of the original image
bc_filt = np.zeros(filterdim, imgA.dtype)
wavelet = pywt.Wavelet('haar')


def GAN(): #returns gaussian noise
    row, col = imgA.shape  # include ch for colour images
    mean = 0
    var = 0.5
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col))  #ch
    gauss = gauss.reshape(row, col)#ch
    return gauss


def noise_add(gauss, imgA):
    noisy = gauss+imgA
    return noisy


def bc_e(filterdim,alpha, beta): #brightness and contrast enhancer
    for y in range(filterdim[0]):
        for x in range(filterdim[1]):
            bc_filt[y, x] = np.clip(alpha * imgA[y, x] + beta, 0, 255) #brightness and contrast filter
            return bc_filt


def wvlttrns(noisy,wavelet):
    coeffs = pywt.dwt2(noisy, mode='constant', wavelet=wavelet)
    LL, (LH, HL, HH) = coeffs  # cA:LL cV:LH cD:HH cH: HL.
    coeffsA = np.asarray(coeffs)
    return coeffsA, LL, HH


size = imgA.shape
number = size[0]*size[1]


def VISUshrink_T(LL,HH,tscale): #implementing VISUshrink algorithm
    TLL = np.sqrt((np.std(LL) ** 2) * (np.log(number)))
    THH = np.sqrt((np.std(HH) ** 2) * (np.log(number)))
    LL1 = pywt.threshold(LL, TLL * tscale, 'soft')
    HH1 = pywt.threshold(HH, THH * tscale, 'soft')
    return LL1, HH1


def iwvlettrns(LL1,HH1,wavelet): #inverse wavelet transform
    inv = pywt.idwt(LL1, HH1, wavelet=wavelet)
    return inv


simgx = size[0] #size of image (x direction)
simgy = size[1] #size of image (y direction)


def scaling(inv): #scales all matrices to a uniform size for matrix manipulation
    invscaled = cv2.resize(inv, (simgy, simgx))
    return invscaled


def blur(invscaled): #bluring
    b_filter =cv2.blur(invscaled, (5, 5))
    return b_filter


def write(F): #F = filter
    filtered = cv2.imwrite('filter1.jpg',F)
    return filtered


bri_con = bc_e(filterdim,1.1,10)
coeffs, LL1, HH1 = wvlttrns(bri_con, wavelet)
LL2, HH2 = VISUshrink_T(LL1,HH1,1/3)
invM = iwvlettrns(LL2,HH2,wavelet) #invM is the reconstructed matrix
FF = scaling(invM)
write(FF)
