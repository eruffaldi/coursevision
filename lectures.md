
# Computer Vision for Humans and Robots

# Lecture Topics

Here we highlight the key concepts

## 1. Introduction

- what is computer vision
- history
- computer vision capabilities and tasks
- compelling examples

- review of python
- review of numpy
- basics of opencv

Notebooks:
- [Basics](Basics.ipynb)

Book:
- Szelisk Chapter 1

## 2. Colors

- spectrum
- anatomy
-- cone types
-- metamers
- tristimulus encoding
- color spaces: YUV, LAB
- digital sensor
-- rolling shutter

Notebooks:
- colors

Book:
- Szelisk Chapter 2.2-2.3

Literature:
- Sensor Fusion Spline with Rolling Shutter

## 3. Image Processing

- types of filter
- linear filter
- classic linear filters: 
- separable filters
- gaussian smoother
- frequency transformation
- box vs gaussian in frequeyncy
- pyramidal processing
- computational cost of filters, separable and FFT
- example of DCT

Literature:
- Learning a Separable Kernel

Demos:
- Live FFT

Notebooks:
- Filtering
- Frequency
- Pyramidal

Book:
- Szelisk Chapter 3

Missing Topics:
- some image transformations

Exercises:
- show the 2D Fourier basis
- matching using filters

## 4. Edges

- edge detection
- Canny edge detector
- bilinear interpolation
- non-maximum suppression

Book:
- Szeliski Chapter 4.2

Lectures:
- Canny Edge Detector Paper (https://pdfs.semanticscholar.org/55e6/6333402df1a75664260501522800cf3d26b9.pdf)

## 5. Points

- harris detector

Book:
- Szelisi Chapter 4.1

## 9. Faces

- the face pipeline: definitions, basic principles
- the Viola-Jones Algorithm: rectangles, integral images, decision tree, AdaBoost, cascade, training set
- eigenfaces

Bonus: discussion about VJ algorithm and comparison to alternatives

Book:
- Szeliski Chapter 14.1 and 14.2

Software:
- OpenCV Haar detector
- DLib Hog and examples
- [OpenFACE](https://github.com/TadasBaltrusaitis/OpenFace)
- Online examples: e.g. [Visage](visagetechnologies.com/html5/)
