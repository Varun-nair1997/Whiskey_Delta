"""
This program denoises images using the wavelet transform and the VISUShrink thresholding algorithm
"""

__author__ = "Varun Nair"

import numpy as np
import cv2
import pywt

def bc_e(imgA, filterdim, alpha, beta):
    """
    brightness and contrast enhancer
    :param imgA: input image
    :param filterdim: size of image
    :param alpha: contrast scaling value between 1.00 and 3.00
    :param beta: brightness scaling value between 0 and 100
    :return: enhanced image
    """
    filter_bright = lambda val, a, b: np.clip(a * val + b, 0, 255)
    func = np.vectorize(filter_bright)
    return func(imgA, alpha, beta)


def GAWN(imgA):
    """
    adds gaussian white noise
    :param imgA: the input image
    :return: image corrupted with gauusian white noise
    """
    row, col = imgA.shape  # include ch for colour images
    mean = 1
    var = 0.15
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, (row, col))  #ch
    gauss = gauss.reshape(row, col)  # ch
    C_I = gauss + imgA
    C_I_copy = C_I
    gauss = 255 * (gauss / gauss.max())
    C_I = gauss + imgA
    C_I = np.clip(C_I, 0, 255)
    C_I = C_I.astype(np.uint8)
    return C_I_copy


def wavelet_transform(noisy, wavelet):
    """
    calculates wavelet transform based on given basis
    :param noisy: noisy image as nparray
    :param wavelet: given basis
    :return: coeffsA, LL, HH
    """
    coeffs = pywt.dwt2(noisy, mode='constant', wavelet=wavelet)
    LL, (LH, HL, HH) = coeffs  # cA:LL cV:LH cD:HH cH: HL.
    coeffsA = np.asarray(coeffs)
    return coeffsA, LL, HH


def VISUshrink_T(filterdim, LL, HH, tscale=1/3):
    """
    VISUShrink thresholding
    :param filterdim: shape of the image
    :param LL: 2x low pass
    :param HH: 2x high pass
    :param tscale: scaling factor for threshold
    :return: updated LL(LL1) and HH(HH1)
    """
    number = filterdim[0] * filterdim[1]
    TLL = np.sqrt((np.std(LL) ** 2) * (np.log(number)))
    THH = np.sqrt((np.std(HH) ** 2) * (np.log(number)))
    LL1 = pywt.threshold(LL, TLL * tscale, 'soft')
    HH1 = pywt.threshold(HH, THH * tscale, 'soft')
    return LL1, HH1


def inv_wavelet_transform(LL1, HH1, wavelet):
    """
    inverse wavelet transform using thresholded values of LL(LL1) and HH(HH1)
    :param LL1: thresholded values of LL
    :param HH1: thresholded values of HH
    :param wavelet: given basis
    :return: unscaled de-noised image
    """
    inv = pywt.idwt(LL1, HH1, wavelet=wavelet)
    return inv


def scaling(inv, filterdim):
    """
    scales the denoised image to original dimensions
    :param inv: unscaled de-noised image
    :param filterdim: shape of the image
    :return: final corrected image
    """
    invscaled = cv2.resize(inv, (filterdim[1], filterdim[0]))
    return invscaled


def wavelet_denoising(img, wavelet=pywt.Wavelet('db5')):
    """
    creates a denoised image. (default wavelet = haar)
    :param img: loaded as a numpy array
    :param wavelet: pyWavelet used for transform
    :return: none
    """
    if not isinstance(img, np.ndarray):
        raise TypeError("The image is not loaded correctly as a numpy array")

    alpha = input("enter a value between 1.00 and 3.00: ")
    beta = input("enter a value 0 and 100: ")
    filterdim = imgA.shape  # dimensions of the original image
    corrupted_img = GAWN(img)
    corrected_img = bc_e(corrupted_img, filterdim, float(alpha), int(beta))
    coeffs, LL, HH = wavelet_transform(corrected_img, wavelet)
    LL1, HH1 = VISUshrink_T(filterdim, LL, HH)
    unscaled_denoised = inv_wavelet_transform(LL1, HH1, wavelet=wavelet)
    denoised_image = scaling(unscaled_denoised, filterdim)
    cv2.imwrite('denoised.jpg', denoised_image)


if __name__ == "__main__":
    img = cv2.imread("DSC1.jpeg", 0)
    imgA = np.asarray(img)  # imgA is the image as an Array
    wavelet_denoising(imgA)

