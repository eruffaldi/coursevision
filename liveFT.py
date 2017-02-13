#!/usr/bin/env python
#coding: utf8

"""
Overview
========
This program uses OpenCV to capture images from the camera, Fourier transform
them and show the Fourier transformed image alongside the original on the screen.
run on mac os x machines from the command line:
    $ ./liveFT.py
To get help on the many command-line options available for tweaking performance:
    $ ./liveFT.py --help
Recommended options for MacBook Air:
    $ ./liveFT.py --color -k -p
Or for a closer crop:
    $ ./liveFT.py --color -r 400 -c 400 -k

Required: A python 2.7 installation (tested on Enthought Canopy),
with: 
    - OpenCV (for camera reading)
    - numpy, matplotlib, scipy, argparse

Tested on an iMac and a macbook air. YMMV

With input from David Mannicke to get it working under Windows 
(through insertion of the imwrite and waitKey functions...)
"""

__author__ = "Brian R. Pauw, David Mannicke"
__contact__ = "brian@stack.nl"
__license__ = "GPLv3+"
__date__ = "2014/01/25"
__status__ = "v2"

#import os
import time
#import re #regular expressions
#import numpy
import numpy as np
#import matplotlib
#matplotlib.use('tkagg') #this works to solve the problem where windows do not update until the end of the script, and must be called before importing pyplot. There is a printed message to verify the right manager has been chosen. The wx backend does not update.
#from matplotlib import pyplot,cm
#from scipy import fftpack
#for direct camera addressing
import cv2 #opencv-based functions
import argparse #process input arguments
#import pdb; pdb.set_trace()

def argparser():
    parser = argparse.ArgumentParser(description = """
            A demonstration program showing a live camera image feed 
            alongside the intensity component of the Fourier transform
            of the camera image.\n
            Required: A python 2.7 installation (tested on Enthought Canopy),
            with: 
                - OpenCV (for camera reading)
                - numpy, TkAgg, matplotlib, scipy, argparse
            Cobbled together by Brian R. Pauw.
            Released under a GPLv3+ license.
            """)
    parser.add_argument("-n", "--numShots", type = int, default = 1e5,
            help = "Max. number of images before program exit")
    parser.add_argument("-o", "--nContrIms", type = int, default = 30,
            help = "Calculate average contrast over N images")
    parser.add_argument("-d", "--camDevice", type = int, default = 0,
            help = "Integer specifying the camera device to use")
    parser.add_argument("-i", "--imAvgs", type = int, default = 1, 
            help = "use an average of N images to show and FFT")
    parser.add_argument("-y", "--vScale", type = float, default = 1.,
            help = "rescale the video vertically using interpolation")
    parser.add_argument("-x", "--hScale", type = float, default = 1.,
            help = "rescale video horizontally using interpolation")
    #image freezes when not downscaled in color!
    parser.add_argument("-p", "--downScale", #default = True,
            action = "store_true", 
            help = "use pyramidal downscaling (once) on the image")
    parser.add_argument("-k", "--killCenterLines", 
            action = "store_true",
            help = "remove central lines from the FFT image")
    parser.add_argument("-f", "--figid", type = str, default = "liveFFT",
            help = "name of the image window")
    parser.add_argument("-r", "--rows", type = int, default = "400",
            help = "use only centre N rows of video image")
    parser.add_argument("-c", "--columns", type = int, default = "400",
            help = "use only centre N columne of video image")
    parser.add_argument("-z", "--minContrast", type = float, default = 7,
            help = "minimum contrast scaling (adjusts black level)")
    parser.add_argument("-a", "--maxContrast", type = float, default = 1,
            help = "maximum contrast scaling (adjusts white level)")
    parser.add_argument("-q", "--color", action = "store_true",
            help = "trade a little speed for color")
    parser.add_argument("-w","--write-image",dest="writeimage",action="store_true")
    
    return parser.parse_args()

class live_FT2(object):
    """
    This function shows the live Fourier transform of a continuous stream of 
    images captured from an attached camera.

    """
    #internal variables and constants:
    color = False
    imMin = .004 #minimum allowed value of any pixel of the captured image
    contrast = np.concatenate((
        np.zeros((10, 1)), np.ones((10, 1))), axis = 1) #internal use.

    def __init__(self, **kwargs):
        #process kwargs:
        for kw in kwargs:
            setattr(self, kw, kwargs[kw])

        self.vc = cv2.VideoCapture(self.camDevice) #camera device
        cv2.namedWindow(self.figid, 0) #0 makes it work a bit better
        cv2.resizeWindow(self.figid, 1024, 768) #this doesn't keep
        #raw_input('Press Enter to start') #wait 
        #start image collection, very device specific here.
        rval, frame = self.vc.read()
        #we need to wait a bit before we get decent images
        print "warming up camera... (.1s)"
        time.sleep(.1)
        rval = self.vc.grab()
        rval, frame = self.vc.retrieve()
        #determine if we are not asking too much
        frameShape = np.shape(frame)
        if self.rows > frameShape[1]:
            self.rows = frameShape[1]
        if self.columns > frameShape[0]:
            self.columns = frameShape[0]

        #calculate crop
        self.vCrop = [np.ceil(frameShape[0]/2. - self.columns/2.),
                np.floor(frameShape[0]/2. + self.columns/2.)]
        self.hCrop = [np.ceil(frameShape[1]/2. - self.rows/2.),
                np.floor(frameShape[1]/2. + self.rows/2.)]
        #start image cleanup with something like this:
        #for a running contrast of nContrIms frames
        self.contrast = np.concatenate( (
            np.zeros((self.nContrIms, 1 )),
            np.ones((self.nContrIms, 1 )) ),
            axis=1)

        Nr = 0
        #main loop
        while Nr <= self.numShots:
            a = time.time()
            Nr += 1
            contrast = self.camimage_ft()
            print('framerate = {} fps \r'.format(1. / (time.time() - a)))
        #stop camera
        self.vc.release()

    def camimage_ft(self):
        
        imAvgs = self.imAvgs
        vCrop = self.vCrop
        hCrop = self.hCrop
        contrast = self.contrast

        #read image
        rval = self.vc.grab()
        rval, im = self.vc.retrieve()
        im = np.array(im, dtype = float)
        #if we want to use an average of multiple images:
        if imAvgs > 1:
            im /= float(imAvgs)
            for imi in np.arange(2, imAvgs+1):
                dummy, aim = self.vc.read()
                im += aim / float(imAvgs) 

        #crop image
        vCrop = [int(x) for x in vCrop]
        hCrop = [int(x) for x in hCrop]
        #print vCrop,im.shape
        im = im[vCrop[0] : vCrop[1], hCrop[0]: hCrop[1], :]
        #scaling horizontal axis down
        if (self.vScale != 1) or (self.hScale != 1):
            im = cv2.resize(im, None, fx = self.hScale, fy = self.vScale)
        #pyramid downscaling
        #if self.downScale or self.color: #color image freezes when not downscaled!
        if self.downScale: #large and color images freeze when not downscaled!
            im = cv2.pyrDown(im)

        if not self.color:
            #reduce dimensionality
            im = np.mean(im, axis = 2, dtype = float)
        #make sure we have no zeros
        im = (im - im.min()) / (im.max() - im.min())
        im = np.maximum(im, self.imMin)
        #FFT hints from http://www.astrobetter.com/fourier-transforms-of-images-in-python/
        #Numpy option, not quite all that much slower but much clearer than openCV
        if self.color:
            Intensity = np.zeros(np.shape(im))
            for ci in range(np.size(im,2)):
                Intensity[:,:,ci] = np.abs( 
                        np.fft.fftshift( np.fft.fft2(im[:,:,ci]) ) 
                        )**2
        else:
            Intensity = np.abs( np.fft.fftshift( np.fft.fft2(im) ) )**2

        #OpenCV option, http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html#fourier-transform
        #dft = cv2.dft( np.float32(im), flags = cv2.DFT_COMPLEX_OUTPUT)
        #dft = np.fft.fftshift(dft)
        #Intensity = cv2.magnitude(dft[:, :, 0], dft[:, :, 1])
        #Intensity = abs(dft[:, :, 0])**2
        Intensity += self.imMin

        if self.killCenterLines:
            #blatantly copied from Samuel Tardif's code
            # kill the center lines for higher dynamic range 
            # by copying the next row/column
            if not self.color:
                h, w = np.shape(Intensity)
                Intensity[(h/2-1):(h/2+1), :] = Intensity[(h/2+1):(h/2+3), :]
                Intensity[:, (w/2-1):(w/2+1)] = Intensity[:, (w/2+1):(w/2+3)]
            else:
                h, w, c = np.shape(Intensity)
                Intensity[(h/2-1):(h/2+1), :, :] = (
                        Intensity[ (h/2+1):(h/2+3), :, :] )
                Intensity[:, (w/2-1):(w/2+1), :] = (
                        Intensity[ :, (w/2+1):(w/2+3), :] )

        #running average of contrast
        ##circshift contrast matrix up
        contrast = contrast[np.arange(1,np.size(contrast,0)+1)%np.size(contrast,0),:]
        ##replace bottom values with new values for minimum and maximum
        contrast[-1,:]=[np.min(Intensity),np.max(Intensity)]

        #openCV draw
        vmin = np.log(contrast[:,0].mean()) + self.minContrast 
        vmax = np.log(contrast[:,1].mean()) - self.maxContrast
        #print('{}'.format(Intensity.dtype)) float32
        Intensity = (np.log(Intensity + self.imMin) - vmin) / (vmax - vmin )
        Intensity = Intensity.clip(0., 1.)
        #Intensity = (Intensity - Intensity.min()) / (Intensity.max() - Intensity.min())

        time.sleep(.01)
        cv2.imshow(self.figid, np.concatenate((im, Intensity),axis = 1))
        #cv2.updateWindow(figid)
        if self.writeimage:
            cv2.imwrite(r"temp.jpg",255 * np.concatenate((im, Intensity),axis = 1))

        cv2.waitKey(1)

        return contrast


if __name__ == '__main__':
    #manager=pyplot.get_current_fig_manager()
    #print manager
    #process input arguments
    adict = argparser()
    #run the program, scotty! I want a kwargs object, so convert args:
    adict = vars(adict)
    live_FT2(**adict) #and expand to kwargs
