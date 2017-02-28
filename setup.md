# Setup

Useremo Python con OpenCV e per alcune cose i notebook di IPython. Preferirei fossimo tutti su Linux/OSX ma anche Windows va bene.

# Linux
	apt-get install opencv
	pip install numpy
	pip install jupyter
	pip install scikit-learn

Bonus: https://pythonhosted.org/spyder/

# Windows
Consiglio Anaconda: https://www.continuum.io/downloads versione Python 2.7. E’ grande ma contiene tutto quello che serve: https://docs.continuum.io/anaconda/pkg-docs 

Si potrebero installare i pacchetti a pezzi usando  http://www.lfd.uci.edu/~gohlke/pythonlibs/ ma alla fine potrebbe mancare qualcosa:
Python 2.7: python-2.7.13.amd64 https://www.python.org/ftp/python/2.7.13/python-2.7.13.amd64.msi 
Matplotlib-2.0.0-cp27-cp27m-win_amd64.whl
Numpy-1.11.3+mkl-cp27-cp27m-win_amd64.whl
Scikit_learn-0.18.1-cp27-cp27m-win_amd64.whl
opencv_python-3.1.0-cp27-cp27m-win_amd64.whl

# OSX
port install opencv
pip install numpy
pip install jupyter
pip install  scikit-learn
