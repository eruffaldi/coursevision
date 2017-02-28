
Examples
nextimg = cv2.Canny(lastimg,100,200,10)


import math

def normalized(x):
  M = np.max(x)
  m = np.min(x)
  print "min",M,"max",m
  return (x-m)/(M-m)
lastimg = data.get("img")
if lastimg is None or False:
	lastimg = cv2.imread("../example.jpg",cv2.IMREAD_GRAYSCALE)
	data["img"] = lastimg

fi = cv2.getGaussianKernel(10, 5)
fi2 = fi * fi.T
print fi2.shape,fi2.dtype
#nextimg = cv2.Canny(lastimg,100,200,10)
dt = cv2.CV_32F
nextimgf = fi2.astype(np.float32)/255.0

#Sobel
nextimgX = cv2.filter2D(nextimgf,dt,np.array([[1,0,-1],[2,0,-2],[1,0,-1]]))
nextimgY = cv2.filter2D(nextimgf,dt,np.array([[1,0,-1],[2,0,-2],[1,0,-1]]).T)

#nextimgX = cv2.filter2D(nextimgf,dt,np.array([[-1,1]]))
#nextimgY = cv2.filter2D(nextimgf,dt,np.array([[1,0,-1],[2,0,-2],[1,0,-1]]).T)
srcimg = lastimg.astype(np.float32)/255.0
nextimgX = cv2.filter2D(srcimg,-1,nextimgX)
nextimgY = cv2.filter2D(srcimg,-1,nextimgY)

nextimgM = np.sqrt(nextimgX**2+nextimgY**2)
minv = np.min(nextimgM)
nextimga = np.arctan2(nextimgY,nextimgX)
#nextimga[nextimgM == 0] = 0
img = np.zeros((nextimga.shape[0],nextimga.shape[1],3),dtype=np.float32)
img[:,:,0] = nextimgX
img[:,:,1] = nextimgY
img = normalized(img)
#r = img[:,:,0]
#r[nextimgM < 1e-3] = 0
#g = img[:,:,1]
#g[nextimgM < 1e-3] = 0
#nextimg = lastimg
#cv2.resizeWindow("live",640,400)
imshow((img))

# %time 