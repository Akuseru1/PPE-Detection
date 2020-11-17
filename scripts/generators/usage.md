#do the script
## in the venv
source prepare_data images/annotations.csv
#separate train and test
test_and_train
# generate label map file
python generate_pbtxt.py csv images/test.csv output/label_map.pbtxt
# generate record file 
python generate_tfrecord.py images/train.csv output/label_map.pbtxt images/train output/train.record
python generate_tfrecord.py images/test.csv output/label_map.pbtxt images/test output/test.record
