import scipy.ndimage as ndi
import scipy
import numpy
import Image
import math

sigma = 1.4
f = 'Bikesgray.jpg'
img = Image.open(f).convert('L')                                          #grayscale
imgdata = numpy.array(img, dtype = float)                                 
G = ndi.filters.gaussian_filter(imgdata, sigma)                           #gaussian low pass filter

sobelout = Image.new('L', img.size)                                       #empty image
sobeloutmag = numpy.array(sobelout, dtype = float)                        
sobeloutdir = numpy.array(sobelout, dtype = float)

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
        mag = math.ceil(math.sqrt((px*px)+(py*py)))
        direc = math.atan2(py, px)
        sobeloutmag[x][y] = mag
        sobeloutdir[x][y] = direc

scipy.misc.imshow(sobeloutmag)

    
        
