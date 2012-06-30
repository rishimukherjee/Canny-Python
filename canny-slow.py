import scipy.ndimage as ndi
import scipy
import numpy
import Image
import math
from math import pi

sigma = 1.4
f = 'Bikesgray.jpg'
img = Image.open(f).convert('L')                                          #grayscale
imgdata = numpy.array(img, dtype = float)                                 
G = ndi.filters.gaussian_filter(imgdata, sigma)                           #gaussian low pass filter

sobelout = Image.new('L', img.size)                                       #empty image
gradx = numpy.array(sobelout, dtype = float)                        
grady = numpy.array(sobelout, dtype = float)

sobel_x = [[-1,0,1],
           [-2,0,2],
           [-1,0,1]]
sobel_y = [[-1,-2,-1],
           [0,0,0],
           [1,2,1]]

width = img.size[1]
height = img.size[0]

#calculate |G| and dir(G)

for x in range(1, width-1):
    for y in range(1, height-1):
        px = (sobel_x[0][0] * G[x-1][y-1]) + (sobel_x[0][1] * G[x][y-1]) + \
             (sobel_x[0][2] * G[x+1][y-1]) + (sobel_x[1][0] * G[x-1][y]) + \
             (sobel_x[1][1] * G[x][y]) + (sobel_x[1][2] * G[x+1][y]) + \
             (sobel_x[2][0] * G[x-1][y+1]) + (sobel_x[2][1] * G[x][y+1]) + \
             (sobel_x[2][2] * G[x+1][y+1])

        py = (sobel_y[0][0] * G[x-1][y-1]) + (sobel_y[0][1] * G[x][y-1]) + \
             (sobel_y[0][2] * G[x+1][y-1]) + (sobel_y[1][0] * G[x-1][y]) + \
             (sobel_y[1][1] * G[x][y]) + (sobel_y[1][2] * G[x+1][y]) + \
             (sobel_y[2][0] * G[x-1][y+1]) + (sobel_y[2][1] * G[x][y+1]) + \
             (sobel_y[2][2] * G[x+1][y+1])
        gradx[x][y] = px
        grady[x][y] = py

sobeloutmag = scipy.hypot(gradx, grady)
sobeloutdir = scipy.arctan2(grady, gradx)

scipy.misc.imsave('cannynewmag.jpg', sobeloutmag)
scipy.misc.imsave('cannynewdir.jpg', sobeloutdir)

for x in range(width):
    for y in range(height):
        if (sobeloutdir[x][y]<22.5 and sobeloutdir[x][y]>=0) or \
           (sobeloutdir[x][y]>=157.5 and sobeloutdir[x][y]<202.5) or \
           (sobeloutdir[x][y]>=337.5 and sobeloutdir[x][y]<=360):
            sobeloutdir[x][y]=0
        elif (sobeloutdir[x][y]>=22.5 and sobeloutdir[x][y]<67.5) or \
             (sobeloutdir[x][y]>=202.5 and sobeloutdir[x][y]<247.5):
            sobeloutdir[x][y]=45
        elif (sobeloutdir[x][y]>=67.5 and sobeloutdir[x][y]<112.5)or \
             (sobeloutdir[x][y]>=247.5 and sobeloutdir[x][y]<292.5):
            sobeloutdir[x][y]=90
        else:
            sobeloutdir[x][y]=135


scipy.misc.imsave('cannynewdirquantize.jpg', sobeloutdir)

mag_sup = sobeloutmag.copy()

for x in range(1, width-1):
    for y in range(1, height-1):
        if sobeloutdir[x][y]==0:
            if (sobeloutmag[x][y]<=sobeloutmag[x][y+1]) or \
               (sobeloutmag[x][y]<=sobeloutmag[x][y-1]):
                mag_sup[x][y]=0
        elif sobeloutdir[x][y]==45:
            if (sobeloutmag[x][y]<=sobeloutmag[x-1][y+1]) or \
               (sobeloutmag[x][y]<=sobeloutmag[x+1][y-1]):
                mag_sup[x][y]=0
        elif sobeloutdir[x][y]==90:
            if (sobeloutmag[x][y]<=sobeloutmag[x+1][y]) or \
               (sobeloutmag[x][y]<=sobeloutmag[x-1][y]):
                mag_sup[x][y]=0
        else:
            if (sobeloutmag[x][y]<=sobeloutmag[x+1][y+1]) or \
               (sobeloutmag[x][y]<=sobeloutmag[x-1][y-1]):
                mag_sup[x][y]=0

scipy.misc.imsave('cannynewmagsup.jpg', mag_sup)

med = numpy.mean(mag_sup)
th = 1.33*med
tl = 0.66*med


