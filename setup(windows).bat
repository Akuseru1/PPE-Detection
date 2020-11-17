:: las imagenes ya deben estar en el folder images, junto con sus .csv
:: - images/
::   - train/
::   - test/
::  - test.csv
::   - train.csv
:: revisar que las imagenes sean del mismo tipo (mime type) antes de empezar
:: el modelo pre-entrenado debe de estar en su folder y el pipeline en el folder models (ver el
:: ejemplo en el mismo folder)

cd "images"
IF NOT EXIST env (
    python -m venv env
    call env\Scripts\activate.bat
    pip install -r ../requirements.txt
) else (
    call env\Scripts\activate.bat
)
IF NOT EXIST "models" (
    git clone --depth=1 https://github.com/tensorflow/models
    setx "PYTHONPATH" "%cd%/models/research:%cd%/models/research/slim:%cd%/models:%PYTHONPATH%"
    cd models/research
    copy object_detection/packages/tf2/setup.py .
    python -m pip install .
    python object_detection/builders/model_builder_tf2_test.py
    cd "../.."
)
cd ".."
python "scripts/generators/generate_pbtxt.py" "csv" "images/test.csv" "annotations/label_map.pbtxt"
python "scripts/generators/generate_tfrecord.py" "images/test.csv" "annotations/label_map.pbtxt" "images/test" "annotations/test.record"
python "scripts/generators/generate_tfrecord.py" "images/train.csv" "annotations/label_map.pbtxt" "images/train" "annotations/train.record"
