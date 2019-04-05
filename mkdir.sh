dir=data
if [[ ! -e $dir ]]; then
    mkdir $dir;
    mkdir $dir/train;
    mkdir $dir/test;
    mkdir $dir/TFRecords;
    mkdir $dir/train/images;
    mkdir $dir/train/json;
    mkdir $dir/test/images;
    mkdir $dir/test/json;
elif [[ ! -d $dir ]]; then
    echo "$dir already exists but is not a directory" 1>&2
fi
python3 copydata.py
python3 jsontoxml.py
python3 xmlcsv1.py
python3 underscore.py
awk -F '[\,]' '{ if(($4=="class")||($4=="boneloss")) print $0}' < data/train_labels.csv > data/bonelosstrain.csv
awk -F '[\,]' '{ if(($4=="class")||($4=="boneloss")) print $0}' < data/test_labels.csv > data/bonelosstest.csv

python3 gtf.py --csv_input="data/bonelosstrain.csv" --set="train" --output_path="data/TFRecords/train.record"

python3 gtf.py --csv_input="data/bonelosstest.csv" --set="test" --output_path="data/TFRecords/test.record"

