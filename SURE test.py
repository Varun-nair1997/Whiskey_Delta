import numpy as np
import cv2

img = cv2.imread("DSC4.JPG",0)
imgB = np.asarray(img)
imgC = cv2.equalizeHist(imgB)
imgA = np.stack((imgB,imgB))
cv2.imwrite('imgA.png',imgA)

imgD = cv2.imread("imgA.png",0)

cv2.imshow("invscal",(imgD))
cv2.waitKey()