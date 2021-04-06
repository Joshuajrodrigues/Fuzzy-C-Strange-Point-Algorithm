# Fuzzy c strange point
import array as arr
import numpy as np
from PIL import Image, ImageDraw
from time import time

start_time = time()
img = Image.open("roiImage.jpg")

img1 = Image.open("blankImg.jpg")
img2 = Image.open("blankImg.jpg")
img3 = Image.open("blankImg.jpg")


width, height = img.size

# green channel extraction
eye = img.load()
for i in range(width):
    for j in range(height):
        r, g, b = eye[i, j]
        eye[i, j] = (r-r, g-0, b-b)
img.save('greeneye.jpg')


# number of clusters = 2 = disk and cup
# getting cmin and cmax
data = np.array(img)
cmin = data[..., 1].min()
cmax = data[..., 1].max()
# print(cmin,cmax) 56 251


tempArrY = arr.array('d', [])

for i in range(width):
    for j in range(height):
        r, g, b = eye[i, j]  # (0,78,0)
        tempArrY.append(g)
cs = np.median(tempArrY)

if np.linalg.norm(cmin-cs) == np.linalg.norm(cmax-cs):
    cstr = cs

elif np.linalg.norm(cmin-cs) < np.linalg.norm(cmax-cs):
    cstr = (cs+(abs(cmax-cs)/2))  # 3 clusers 2

elif np.linalg.norm(cmin-cs) > np.linalg.norm(cmax-cs):
    cstr = (cmin+(abs(cs-cmin)/2))  # 3 clusers 2

print(cmin, cmax, cstr)

for i in range(width):
    for j in range(height):
        x = eye[i, j]  # (0,78,0)
        coords = i, j
        cminx = (x[1]-cmin)**2
        cmaxx = (x[1]-cmax)**2
        cstrx = (x[1]-cstr)**2

        uc1 = 1/((cminx/cminx)+(cminx/cmaxx)+(cminx/cstrx))
        uc2 = 1/((cmaxx/cmaxx)+(cmaxx/cminx)+(cmaxx/cstrx))
        uc3 = 1/((cstrx/cstrx)+(cstrx/cminx)+(cstrx/cmaxx))
        #print(uc3, uc2, uc1)
        if np.isnan(uc1) or np.isnan(uc2) or np.isnan(uc3):
            continue
        elif (uc1 > uc3) and (uc1 > uc2):
            continue

        elif (uc2 > uc1) and (uc2 > uc3):

            img2.putpixel(coords, x)

        else:

            img3.putpixel(coords, x)


img2.save("Fuzzy_C_strange_point_cup.jpg")
img3.save("Fuzzy_C_strange_point_disk.jpg")
# cali()
proc_time = time()-start_time
print(proc_time)
# 7.949074029922485
