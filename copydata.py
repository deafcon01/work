import os
from shutil import copyfile
import pdb
import re
train_list=['27-03-2019 (mar)','26-03-2019.. (mar)','01-04-2019','02-04-2019']
test_list=['9th april,2019']
def cpy(lists,f):
    path =os.getcwd()
    for folder in lists:
        for files in os.listdir(folder):
            #pdb.set_trace()
            if files.endswith('.jpg') > 0:
                copyfile(os.path.join(path,folder,files),os.path.join(path,'data',f,'img',re.sub(r"[^\S\n\t]+",'_',files)))#.replace(' ','_')))
            elif files.endswith('.json') > 0:
                copyfile(os.path.join(path,folder,files),os.path.join(path,'data',f,'json',re.sub(r"[^\S\n\t]+",'_',files)))#.replace(' ','_')))
                


cpy(train_list,'train')
cpy(test_list,'test')
