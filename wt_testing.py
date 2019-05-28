import pywt
import numpy as np

data = np.ones((4,4),dtype=np.float64)
#wavelet = pywt.Wavelet('shan')
wavelet = pywt.ContinuousWavelet('shan1.5-1.0')
coeffs = pywt.dwt2(data, 'coif1')
cA,(cH,cV,cD) = coeffs

print(data)
print("-")
#print(coeffs)
print(cA)
print("-")
print(cH)
print("-")
print(cV)
print("-")
print(cD)
print("-")
print("size", cA.size, cH.size, cV.size, cD.size)
print("-")
print(wavelet)