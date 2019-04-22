import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import Image
import cv2
from shutil import copyfile
import pdb
import re
from json2xml import json2xml,readfromjson
import numpy as np

#train_list=['27-03-2019 (mar)','26-03-2019.. (mar)','01-04-2019','02-04-2019']
#test_list=['9th april,2019']
 
def cpy(lists,f):
    path =os.getcwd()
    for folder in lists:
        for files in os.listdir(folder):
            ##
            if files.endswith('.jpg') > 0:
                copyfile(os.path.join(path,folder,files),os.path.join(path,'data',f,'img',re.sub(r"[^\S\n\t]+",'_',files)))#.replace(' ','_')))
            elif files.endswith('.json') > 0:
                copyfile(os.path.join(path,folder,files),os.path.join(path,'data',f,'json',re.sub(r"[^\S\n\t]+",'_',files)))#.replace(' ','_')))


def clahe():
    cdir=os.getcwd()
    outdir='images/'
    for directory in ['data/train']:#,'data/test']:
        #
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

def jsontoxml():
    cdir=os.getcwd()
    outdir='annotations'
    for directory in ['data/train']:#,'data/test']:
        if not os.path.exists(os.path.join(cdir,directory,outdir)):
            os.mkdir('{}/{}/{}'.format(cdir,directory,outdir))
            ##
        for files in os.listdir(os.path.join(cdir,directory,'json')):
            if files.endswith('.json'):
                data=readfromjson(os.path.join(cdir,directory,'json',files))
                xml=json2xml.Json2xml(data).to_xml()
                name=files.replace('.json','.xml')
                txt_file= open(os.path.join(cdir,directory,outdir,name),'w')
                txt_file.write(xml)
                txt_file.close()


def xml_to_csv(path):
    xml_list = []
    delta=0.002
    ann_path = path.replace("images","annotations")
    for xml_file in os.listdir(ann_path):
        #print(xml_file)
        tree = ET.parse(os.path.join(ann_path,xml_file))
        root = tree.getroot()
        if root.find('object'):
            #print('found object')
            for member in root.findall('object'):
                #fname = root.find('filename').text
                #fname.replace(' ','_')
                value = (root.find('filename').text,
                        int(root.find('size')[0].text),
                        int(root.find('size')[1].text),
                        member[0].text,
                        int(member[4][0].text),
                        int(member[4][1].text),
                        int(member[4][2].text),
                        int(member[4][3].text)
                        ) 
                xml_list.append(value)
        elif root.find('annotations'):
            filename= xml_file.replace('.xml','.jpg')
            im = Image.open(os.path.join(path,filename))
            w,h=im.size
            im.close()
            for member in root.findall('annotations'):
                #fname = root.find('meta/imageid').text
                #print(fname)
                #fname.replace(' ','_')
                value = (root.find('meta/imageid').text,
                        int(w),
                        int(h),
                        member[1].text,
                        float(member[3].text)-delta,
                        float(member[5].text)-delta,
                        float(member[4].text)+delta,
                        float(member[0].text)+delta
                        )
                xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def underscore():
    filenames = ['data/train_labels.csv','data/test_labels.csv']
    for filename in filenames:
        with open(filename,'r') as f:
            lines = f.readlines()
        #lines = [line.replace(' ','_') for line in lines]
        #lines = [line.replace('__','_') for line in lines]
        lines = [re.sub(r"[^\S\n\t]+",'_',line) for line in lines]
        with open(filename,'w') as f:
            f.writelines(lines)

def generate_txt_files(path_to_toy_data):
    files = os.listdir(path_to_toy_data)
    train = open("data/train/train.txt", "w")
    train_val = open("data/train/trainval.txt", "w")
    val = open("val.txt", "w")
    #pdb.set_trace()
    size_train_set = int(len(files) * 0.7)
    size_train_val_set = int(len(files) * 1)
    size_val_set = int(len(files) * 0.25)
    #pdb.set_trace()
    train_files = np.random.choice(files, size=size_train_set, replace=False)
    for f in train_files:
        train.write(re.sub(".jpg$", "",f) + " " + str(1) + "\n")
        #files.remove('data/train/images'+f)
    train.close()
    #pdb.set_trace()
    train_val_files = np.random.choice(files, size=size_train_val_set, replace=False)
    for f in files:
        train_val.write(re.sub(".jpg$", "",f) + " " + str(1) + "\n")
        #files.remove('data/train/images'+f)
    train_val.close()
    """
    val_files = np.random.choice(files, size=size_val_set, replace=False)
    for f in val_files:
        val.write(re.sub(".jpg$", "",f) + " " + str(1) + "\n")
        files.remove(f+'.jpg')
    val.close()
    print(len(files))
    """

def main():
    train_list=['13-04-2019','01-04-2019','02-04-2019','9th april,2019','27-03-2019 (mar)','16-04-2019','18th april','22nd april','26-03-2019.. (mar)']
    test_list=['26-03-2019.. (mar)']
    ##
    cpy(train_list,'train')
    #cpy(test_list,'test')
    clahe()
    jsontoxml()
    generate_txt_files("data/train/images")
    """
    for directory in ['data/train']:
        image_path = os.path.join(os.getcwd(), '{}/images'.format(directory))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv('{}_labels.csv'.format(directory), index=None)
        print('Successfully converted xml to csv.')
    underscore()
    """

if __name__ == "__main__":
    main()
