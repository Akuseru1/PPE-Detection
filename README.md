1. coloca las imagenes de train y test en directorios asi
    images/train
    images/test
2. colocar los train.csv y test.csv en el directorio images/ , los csv deben tener las columnas
   'filename' y 'class'
3. utiliza el script de setup (puede que haya que hacer source al script)
4. crea el label_map y los tf_records haciendo uso de los scripts generadores, los cuales se
   encuentran en el folder scripts/ , el manual de uso es usage.md
    - generate_pbtxt.py
    - generate_tfrecord.py

   se deben  generar un label_map.pbtxt, test.record y train.record

5. clonar el repositorio de tensorflow object detection en google drive

6. se deben crear los archivos pbtxt y tfrecord

7. poner un modelo pre entrenado en pre-trained-models/

8. poner un pipeline configurado en models/

9. entrenar con:

   ```!python scripts/train/model_main_tf2.py --model_dir=models/my_ssd_mobilenet_v2_fpnlite --pipeline_config_path=models/my_ssd_mobilenet_v2_fpnlite/pipeline.config --logtostderr```

10. exportar grafó de inferencia con:

   ```!python scripts/train/exporter_main_v2.py --input_type image_tensor --pipeline_config_path=models/my_ssd_mobilenet_v2_fpnlite/pipeline.config --trained_checkpoint_dir=models/my_ssd_mobilenet_v2_fpnlite --output_directory=exported-models/my_mobilenet_model```

11. correr los scripts para hacer test al modelo creado

# opciónal
6. sube los archivos generados a google drive en un path deseado, abre el PPETrainingTensorflow2.ipynb
    en google colab, modifica el path designado en el script para dirigirlos
    hacia los archivos pbtxt y tfrecord, y el path a el repo de tensorflow clonado en google
    drive adicionalmente hay que poner un modelo ya entrenado en
    pre-trained-models (estan en el repo de tensorflow object detection api), y se debe crear
    un pipeline.config en models (todo en el drive de google)

