import pywt
import numpy as np

data = np.ones((4,4),dtype=np.float64)
wavelet = pywt.Wavelet('db5')
#wavelet = pywt.ContinuousWavelet('fbsp')
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
#print(pywt.wavelist())

phi, psi, x = wavelet.wavefun(level=2)
print(phi)
print(psi)
a = phi.reshape((21,1))
print(a)