import numpy as np
import matplotlib.pyplot as plt
from PIL import Image ,ImageFilter
import math

kernel_moy = np.full((3,3,3),1) / 9

def rt(px) :
    if to_grey_pix(px) > 180 :
        return [120,25,120]
    else :
        return [0,0,0]

def to_grey(pixel) :
    col = pixel[0]*0.299 + pixel[1]*0.587 + pixel[2]*0.114
    return [col,col,col] 

def to_grey_pix(pixel) :
    col = pixel[0]*0.299 + pixel[1]*0.587 + pixel[2]*0.114
    return col


def incr_pixel(img ,incr) :
    for i in range(len(img)) :
        for j in range(len(img[0])) :
            img[i][j][0] = max(min(255, img[i][j][0]+incr), 0)
            img[i][j][1] = max(min(255, img[i][j][1]+incr), 0)
            img[i][j][2] = max(min(255, img[i][j][2]+incr), 0)
    return img

def histogram(img_array) :
    r = np.zeros(256).astype(int)
    g = np.zeros(256).astype(int)
    b = np.zeros(256).astype(int)

    for i in range(len(img_array)) :
        for j in range(len(img_array[0])) :
            r[(img_array[i][j][0])] += 1
            g[(img_array[i][j][1])] += 1
            b[(img_array[i][j][2])] += 1
    return [r,g,b]


def imageToGrey(img) :
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            img[i][j] = to_grey(img[i][j])
    return img

def filter(img,temp) :
    plain = np.full((img.shape[0] , img.shape[1] , 3) , 0 ,dtype=np.uint8)
    for x in range(3) :
        for i in range((len(temp[x])//2),len(img)-(len(temp[x])//2)) :
            for j in range((len(temp[x])//2),len(img[0])-(len(temp[x])//2)) :
                res = 0
                for a in range(-(len(temp[x])//2),(len(temp[x])//2)+1) :
                    for b in range(-(len(temp[x])//2),(len(temp[x])//2)+1) :
                        res += temp[x][a+(len(temp[x])//2)][b+(len(temp[x])//2)] * img[i+a][j+b][x]
                plain[i][j][x] = min(int(res) , 255)
    return plain

def gaus(img ,r) :
    img = Image.fromarray(img)
    img = img.filter(ImageFilter.GaussianBlur(radius = r))
    img = np.array(img)
    return img

def histo(img_array) :
    r = np.zeros(256).astype(int)
    g = np.zeros(256).astype(int)
    b = np.zeros(256).astype(int)
    for i in range(len(img_array)) :
        for j in range(len(img_array[0])) :
            r[(img_array[i][j][0])] += 1
            g[(img_array[i][j][1])] += 1
            b[(img_array[i][j][2])] += 1
            
    return [r,g,b]

def contrast(n,maxx,minn):
    return np.clip(int((n-minn)*(255/(maxx-minn))) , 0,255)


def minmax(arr) :
    min = 0
    max = 255
    
    for i in range(len(arr)) :
        if arr[i] != 0:
            min  = i
    for i in range(len(arr)-1,-1,-1) :
        if arr[i] != 0:
            max  = i
    return [min,max]
            
#CREATE TABLE
def contrastDecs(img) :
    histos = histo(img)
    mm = []
    for i in range(3):
        mm.append([0,0])
        mm[i] = minmax(histos[i])
    decs = [{},{},{}]
    for i in range(256) :

        decs[0][str(i)] = contrast(i, mm[0][0], mm[0][1])
        decs[1][str(i)] = contrast(i, mm[1][0], mm[1][1])
        decs[2][str(i)] = contrast(i, mm[2][0], mm[2][1])
    return decs

#METHODE TABLE
def applyDecRGB(img ,decs) :
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            img[i][j][0] = decs[0][str(img[i][j][0])]
            img[i][j][1] = decs[1][str(img[i][j][1])]
            img[i][j][2] = decs[2][str(img[i][j][2])]
    return img

def seuillage(img, t) :
    for i in range(img.shape[0]) :
        for j in range(img.shape[1]) :
            if to_grey_pix(img[i][j]) >= t :
                img[i][j] = [255,255,255]
            else :
                img[i][j] = [0,0,0]
    return img


def edge(img) : 
    img = Image.fromarray(img)
    img = img.filter(ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), 1, 0))

    return np.array(img)

    





