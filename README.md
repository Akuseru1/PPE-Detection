El requirements-gpu.txt solo sirve para gpus de nvidia entonces por ahora solo pruebe con el requirements.txt normal

Una vez haya creado el ambiente de desarrollo tiene que descargar los pesos a la carpeta weights, al drive subi nuevos pesos, puede probar con esos o con los que ya tenia.
Cuando ya tenga los pesos en esa carpeta ejecuta el comando: load_weights.py --weights weights/<archivo.weights> --output weights/ppe.tf --num_classes 4

Cuando este listo el paso anterior ejecute este comando y deberia funcionar la camara con el respectivo modelo.
Solo ejecutar el comando python detect_video.py --video 0 --weights weights/ppe.tf o la ruta al archivo ppe.tf
