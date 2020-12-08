import cv2 as cv
import numpy
from matplotlib import pyplot as plt
from matplotlib.colors import NoNorm


# metoda, ktera vrati histogram jasu obrazku
def get_hist(image):
    hist = numpy.zeros(256)    
    for i in range(len(image)):
            for j in range(len(image[0])):
                hist[int(image[i,j])] += 1
    return hist

# metoda, ktera vyrovna jas v obrazku
def eq_hist(hist, image):    
    # zjisteni nejmnizsiho a nejvyssiho jasu v obrazku
    i=0
    while(hist[i]==0):
        i+=1
    j=255
    while(hist[j]==0):
        j-=1
    # vyrovnani jasu
    for k in range(len(image)):
            for l in range(len(image[0])):
                image[k,l] = (image[k,l]-i)*(255.0/(j-i))                
    return image

# nacteni obrazku
img_uneq = cv.imread("uneq.jpg", 0)

# spocitani histogramu
hist_uneq = get_hist(img_uneq)

# vyrovnani histogramu (cert mi byl dluzen pythonovska mutable pole)
img_eq = eq_hist(hist_uneq,img_uneq.copy())

# spocitani histogramu vyrovnaneho obrazku
hist_eq = get_hist(img_eq)

# vykresleni histogramu
hfig, haxs = plt.subplots(ncols=2)
haxs[0].set_title('unequalized histogram')
haxs[0].bar([i for i in range(len(hist_uneq))],hist_uneq/float(sum(hist_uneq)))
haxs[0].set_xlim(0,256)

haxs[1].set_title('equalized histogram')
haxs[1].bar([i for i in range(len(hist_eq))],hist_eq/float(sum(hist_eq)))
haxs[1].set_xlim(0,256)
haxs[1].set_yticks([])

# vykresleni obrazku
ifig, iaxs = plt.subplots(ncols=2)
iaxs[0].set_title('unequalized image')
# docela na prd je, ze imshow() standardne histogram narovnava, takze se to tu musi vypnout :-)
iaxs[0].imshow(img_uneq,cmap='gray',norm=NoNorm())
iaxs[0].set_xticks([])
iaxs[0].set_yticks([])

iaxs[1].set_title('equalized image')
# tady teoreticky ne, ale budeme konzistentni ;-)
iaxs[1].imshow(img_eq,cmap='gray',norm=NoNorm())
iaxs[1].set_xticks([])
iaxs[1].set_yticks([])

plt.show()
