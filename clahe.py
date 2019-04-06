import os
import cv2
import pdb
#from json2xml import json2xml,readfromjson
cdir=os.getcwd()
outdir='images/'
for directory in ['data/train','data/test']:
    #pdb.set_trace()
    if not os.path.exists(os.path.join(cdir,directory,outdir)):
        os.mkdir('{}/{}/{}'.format(cdir,directory,outdir))
    for files in os.listdir(os.path.join(cdir,directory,"img")):
        bgr = cv2.imread(os.path.join(cdir,directory,"img",files))
        lab = cv2.cvtColor(bgr,cv2.COLOR_BGR2LAB)
        lab_planes = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(16,16))
        lab_planes[0]=clahe.apply(lab_planes[0])
        lab = cv2.merge(lab_planes)
        bgr = cv2.cvtColor(lab,cv2.COLOR_LAB2BGR)
        cv2.imwrite(os.path.join(cdir,directory,outdir,files),bgr)

