Whiskey Delta
# Wavelet-Based Image Denoising using VISUShrink
#### Author: Varun Nair
date created: 26/5/19 (DD/MM/YY)


This repository contains a Python implementation of image denoising using the Discrete Wavelet Transform (DWT) and the VISUShrink soft-thresholding algorithm.

The pipeline adds Gaussian white noise to an image, applies brightness and contrast enhancement, performs wavelet decomposition, applies thresholding to selected coefficients, and reconstructs a denoised image via inverse wavelet transform.

---

## Mathematical Formulation

Let the noisy image be represented as:

I_noisy(x, y) = I(x, y) + n(x, y)

where n(x, y) is additive Gaussian white noise.

---

### Discrete Wavelet Transform (2D)

The 2D DWT decomposes the image into four subbands:

- LL: Approximation (low-frequency components)
- LH: Vertical detail
- HL: Horizontal detail
- HH: Diagonal detail

This implementation uses:
`pywt.dwt2()`


---

### VISUShrink Thresholding

The VISUShrink method applies soft-thresholding using a universal threshold:

T = σ √(2 log N)

where:

- σ is the estimated noise standard deviation  
- N is the number of pixels  

Soft-thresholding is defined as:

ŵ = sign(w) · max(|w| − T, 0)

Thresholding is applied to selected wavelet subbands to suppress noise while preserving structural information.

---

### Inverse Wavelet Transform

The denoised image is reconstructed using:
`pywt.idwt()`


The image is then resized back to its original dimensions.

---

## Numerical Pipeline

1. Add Gaussian White Noise (GAWN)
2. Apply Brightness and Contrast Enhancement
3. Perform 2D Wavelet Decomposition
4. Compute VISUShrink Threshold
5. Apply Soft Thresholding
6. Reconstruct via Inverse Wavelet Transform
7. Resize to Original Dimensions
8. Save Output Image

---

## Features

- Gaussian white noise simulation
- Brightness and contrast scaling
- Wavelet-based multiresolution analysis
- VISUShrink soft-thresholding
- Configurable wavelet basis (default: db4)
- Automatic image reconstruction and saving

---

## Requirements

- Python 3.8+
- NumPy
- OpenCV
- PyWavelets

Install dependencies with:
`pip install numpy opencv-python pywavelets`


---

## Usage

Place the input image (default: `DSC8.JPG`) in the project directory.

Run the script:
`python wavelet_denoising.py`

The program will prompt for:

- Contrast scaling factor (alpha) between 1.00 and 3.00  
- Brightness scaling factor (beta) between 0 and 100  

After execution:

- A corrupted image is displayed  
- The denoised image is saved as:
denoised.jpg


---

## Core Function
`wavelet_denoising(img, wavelet=pywt.Wavelet('db4'))`


### Parameters

- `img`: Input grayscale image as a NumPy array  
- `wavelet`: PyWavelets basis (default: Daubechies-4)

---

## Output

The script produces:

- A noise-corrupted intermediate image  
- A denoised reconstructed image (`denoised.jpg`)

---

## Limitations

- Single-level wavelet decomposition  
- Thresholding applied only to LL and HH subbands  
- Designed for grayscale images  
- Noise model assumes additive Gaussian noise  
- No quantitative metrics (PSNR/SSIM) included  

---






