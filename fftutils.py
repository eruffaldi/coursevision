import numpy as np
import cv2


def fft2centeredlogm(img,outsize=None):
    if outsize is None:
        optsize = (cv2.getOptimalDFTSize(img.shape[0]),cv2.getOptimalDFTSize(img.shape[1]))
    if len(img.shape) == 3:
        axes = (0,1)
    else:
        axes = (-2,-1)
    q = np.fft.fft2(img,s=optsize,axes=axes)
    return np.fft.fftshift(np.log(np.absolute(q)**2),axes)

