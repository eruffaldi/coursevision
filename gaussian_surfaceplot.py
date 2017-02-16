

import numpy as np
import matplotlib.pyplot as plt
import cv2
from IPython.display import Image
from IPython.display import display
imshowg = lambda x: plt.imshow(x,cmap=plt.get_cmap('gray'))
conv2D = lambda x,k: cv2.filter2D(x, -1, k)
from mpl_toolkits.mplot3d import Axes3D
                                  
fig = plt.figure()

img_in  = cv2.imread('example.jpg',cv2.IMREAD_GRAYSCALE)   

fi = cv2.getGaussianKernel(30, 5)
fi2 = fi * fi.T
xx, yy = np.mgrid[0:fi2.shape[0], 0:fi2.shape[1]]

ax = fig.add_subplot(2, 1, 1,projection="3d")
ax.plot_surface(xx, yy, fi2 ,rstride=1, cstride=1, cmap=plt.cm.gray,linewidth=0)

ax = fig.add_subplot(2, 1, 2,projection="3d")

fi2g = conv2D(fi2,np.array([[-1,1]]))
ax.plot_surface(xx, yy, fi2g ,rstride=1, cstride=1, cmap=plt.cm.gray,linewidth=0)
plt.show()
