import os
from shutil import copyfile
import pdb
train_list=['27-03-2019 (mar)','26-03-2019.. (mar)','01-04-2019']
test_list=['02-04-2019']
def cpy(lists,f):
    path =os.getcwd()
    for folder in lists:
        for files in os.listdir(folder):
            #pdb.set_trace()
            if files.find('.jpg') > 0:
                copyfile(os.path.join(path,folder,files),os.path.join(path,'data',f,'images',files.replace(' ','_')))
            elif files.find('.json') > 0:
                copyfile(os.path.join(path,folder,files),os.path.join(path,'data',f,'json',files.replace(' ','_')))
                


cpy(train_list,'train')
cpy(test_list,'test')
