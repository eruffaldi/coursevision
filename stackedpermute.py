# Stacked Tensor Permutation
# Emanuele Ruffaldi 2016
import numpy
import itertools

class SubDim:
	def __init__(self,name,size):
		self.name = name
		self.size = size
	def __hash__(self):
		return (self.name,self.size).__hash__()
	def __repr__(self):
		return "subdim(%s,%d)" % (self.name,self.size)

def makeflatsubdims(a,names):
	return [SubDim(names[i],a.shape[i]) for i in range(0,len(names))]

def makesubdims(pairs):
	r = []
	for x in pairs:
		r = r + [SubDim(name,size) for name,size in x]
	return r

def normalize(inshape):
	return tuple([(x,) if isinstance(x,SubDim) else x for x in inshape])

def parseshapes(inshape):
	expandsizes = []
	inputsubdims = dict()
	compactsizes = []
	ordereddims = []
	q = 0
	for i,x in enumerate(normalize(inshape)):
		w = 1
		for j,s in enumerate(x):
			inputsubdims[s] = q
			expandsizes.append(s.size)
			ordereddims.append(s)
			w *= s.size
			q += 1
		compactsizes.append(w)
	return expandsizes,inputsubdims,compactsizes,ordereddims

def getstrides(inshape):
	# row major (start from last)
	si = 1
	ox = [] # nested as inshape
	od = {} # per subdim
	for i,x in enumerate(normalize(inshape[-1::-1])):
		oy = []
		for j,s in enumerate(x[-1::-1]):
			oy.append(si)
			od[s] = si
			si *= s.size
		ox.append(oy)
	return ox,od

def stackedpermute(a, inshape, outshape=None,verbose=False):	



	ie,ii,ic,io = parseshapes(inshape)
	if outshape is not None:
		oe,oi,oc,oo = parseshapes(outshape)
		if set(io) != set(oo):
			raise "Sub Mismatch of dimensions"
	aflat = numpy.reshape(a,ie)
	if verbose:
		print "sharing the base?",aflat.base is not None,aflat.base is a.base
	if outshape is None:
		return aflat
	aa = [ii[o] for o in oo]
	if aa != range(0,len(ie)):
		aordered = numpy.transpose(aflat,axes=aa)
		if verbose:
			print "sharing the base?",aordered.base is not None,aordered.base is a.base
	else:
		if verbose:
			print "no transpose"
		aordered = aflat
	return numpy.reshape(aordered,oc)

# generate with indices in 
def genmatrix(a):
	w = []
	#a = a[-1::-1]
	for i,x in enumerate(a):
		q = 10**(len(a)-i-1)
		w.append([(j+1)*q for j in range(0,x)])
	o = []
	for y in itertools.product(*w):
		o.append(sum(y))
	o = numpy.array(o)
	return numpy.reshape(o,a)

if __name__ == '__main__':
	# create a matrix with all the indices (max size 9)
	a = genmatrix([2,3,4])
	# consider the tensor as full
	da,db,dc = makeflatsubdims(a,("a","b","c"))
	af = (da,db,dc)
	print "from",af,a.shape
	print a
	rf = (da,(db,dc))
	r = stackedpermute(a,af,rf,verbose=True)
	print "then",rf,r.shape
	print r
	print "input strides", a.strides
	print "output strides", r.strides
	rf = (da,(dc,db))
	r = stackedpermute(a,af,rf,verbose=True)
	print "then",rf,r.shape
	print r
	print "stides",getstrides(rf)
	print "input strides", a.strides
	print "output strides", r.strides

	# Simpler Simpler

	