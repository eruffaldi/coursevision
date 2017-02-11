# Build pyramid in place
import cv2
import numpy as np

def pyrall(src,minsize):
	c0 = src.shape[2] if len(src.shape) == 3 else 0
	levels = []
	h0 = src.shape
	hf = ((src.shape[0]+1)/2,(src.shape[1]+1)/2)

	# enlarge right
	if c0 > 0:
		out = np.zeros((src.shape[0]+1,src.shape[1]+hf[1],c0),dtype=src.dtype)
		slicer = lambda r: out[r[0]:r[1],r[2]:r[3],:]
	else:
		out = np.zeros((src.shape[0]+1,src.shape[1]+hf[1]),dtype=src.dtype)
		slicer = lambda r: out[r[0]:r[1],r[2]:r[3]]
	r = (0,h0[0],0,h0[1])
	q = slicer(r)
	q[:] = src
	levels.append(r)
	r = (-1,0,r[3],-1)
	src = q
	while min(src.shape[0:2]) > minsize:
		hf = ((src.shape[0]+1)/2,(src.shape[1]+1)/2)
		r = (r[1],r[1]+hf[0],r[2],r[2]+hf[1])
		dst = slicer(r)
		cv2.pyrDown(src,dst)
		levels.append(r)
		src = dst
	return out,levels

if __name__ == '__main__':
	img_in  = cv2.imread('example.jpg')#cv2.IMREAD_GRAYSCALE)
	out,levels = pyrall(img_in,4)
	print (levels,[(x[1]-x[0],x[3]-x[2]) for x in levels])
	cv2.imwrite('exampleout.jpg',out)