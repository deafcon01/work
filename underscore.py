import re
filenames = ['data/train_labels1.csv','data/test_labels1.csv']
for filename in filenames:
    with open(filename,'r') as f:
        lines = f.readlines()
    #lines = [line.replace(' ','_') for line in lines]
    #lines = [line.replace('__','_') for line in lines]
    lines = [re.sub(r"[^\S\n\t]+",',',line) for line in lines]
    with open(filename,'w') as f:
        f.writelines(lines)
