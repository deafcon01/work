#Comment these out when not running for first time
#apt install -y vim
#apt install -y libsm6 libxext6 libxrender-dev
#pip3 install opencv-python
#pip3 install json2xml lxml contextlib2
#zip=unzip
#if [[ $zip -ne 0 ]]; then
#    apt -y install unzip
#fi
unzip=01-04-2019
if [[ ! -d $unzip ]]; then
    unzip 01-04-2019.zip;
    unzip 02-04-2019.zip;
    unzip '26-03-2019.. (mar).zip';
    unzip '27-03-2019 (mar).zip';
    unzip '9th april,2019.zip';
    unzip 13-04-2019.zip;
fi
rm '9th april,2019/k.suresh reddy 322900 20180615 12-04-09.JPG'
mv '9th april,2019/m srinivas 405920 20180629 15-35-22.jpg' '9th april,2019/m srinivas 405920 20180629 15-36-15.jpg'
dir=data
if [[ ! -e $dir ]]; then
    mkdir $dir;
    mkdir $dir/train;
    mkdir $dir/test;
    mkdir $dir/TFRecords;
    mkdir $dir/train/img;
    mkdir $dir/train/json;
    mkdir $dir/test/img;
    mkdir $dir/test/json;
elif [[ ! -d $dir ]]; then
    echo "$dir already exists but is not a directory" 1>&2
fi

#python3 copydata.py
#python3 clahe.py
#python3 jsontoxml.py
#python3 xmlcsv1.py

python3 newcode.py

#for file in $dir/train/images/*; do mv "$file" `echo $file | tr '__' '_'` ; done
#for file in $dir/test/images/*; do mv "$file" `echo $file | tr '__' '_'` ; done
#for file in $dir/train/annotations/*; do mv "$file" `echo $file | tr '__' '_'` ; done
#for file in $dir/train/annotations/*; do mv "$file" `echo $file | tr '__' '_'` ; done

#python3 underscore.py

awk -F '[\,]' '{ if($4=="bone_loss"){ $4="boneloss";print $0} else {print $0}}' < data/train_labels.csv > data/train_labels1.csv
awk -F '[\,]' '{ if($4=="bone_loss"){ $4="boneloss";print $0} else {print $0}}' < data/test_labels.csv > data/test_labels1.csv
python3 underscore.py
awk -F '[\,]' '{ if(($4=="class")||($4=="boneloss")||($4=="missing_tooth")){print $0}else{$4="other"; print $1","$2","$3","$4","$5","$6","$7","$8 }}' < data/train_labels1.csv > data/bonelosstrain.csv
awk -F '[\,]' '{ if(($4=="class")||($4=="boneloss")||($4=="missing_tooth")) print $0}' < data/test_labels1.csv > data/bonelosstest.csv
cp data/bonelosstrain.csv .
cp data/bonelosstest.csv .
awk -F '[\,]' '{if($4=="boneloss") print $0}' < bonelosstest.csv > testbone.csv
awk -F '[\,]' '{if($4=="boneloss") print $0}' < bonelosstrain.csv > trainbone.csv
awk -F '[\,]' '{if($4=="missing_tooth") print $0}' < bonelosstest.csv > testmiss.csv
awk -F '[\,]' '{if($4=="missing_tooth") print $0}' < bonelosstrain.csv > trainmiss.csv
python3 gtf.py --csv_input="data/bonelosstrain.csv" --set="train" --output_path="data/TFRecords/train.record"

python3 gtf.py --csv_input="data/bonelosstest.csv" --set="test" --output_path="data/TFRecords/test.record"
tar -zcvf TFRecords.tar.gz data/TFRecords
