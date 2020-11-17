#!/usr/bin/env python
# coding: utf-8
"""
Object Detection (On Video) From TF2 Saved Model
=====================================
"""

# ubidots api stuffs
import datetime
import csv
import warnings
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from object_detection.utils import visualization_utils as viz_utils
from object_detection.utils import label_map_util
import time
import argparse
import cv2
import tensorflow as tf
import pathlib
from UbidotsApi.utils import ubi


import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Suppress TensorFlow logging (1)

tf.get_logger().setLevel("ERROR")  # Suppress TensorFlow logging (2)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model",
    help="Folder that the Saved Model is Located In",
    default="exported-models/my_mobilenet_model",
)
parser.add_argument(
    "--labels",
    help="Where the Labelmap is Located",
    default="exported-models/my_mobilenet_model/saved_model/label_map.pbtxt",
)
parser.add_argument(
    "--threshold", help="Minimum confidence threshold for displaying detected objects", default=0.5
)

args = parser.parse_args()
# Enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices("GPU")
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# PROVIDE PATH TO MODEL DIRECTORY
PATH_TO_MODEL_DIR = args.model

# PROVIDE PATH TO LABEL MAP
PATH_TO_LABELS = args.labels

# PROVIDE THE MINIMUM CONFIDENCE THRESHOLD
MIN_CONF_THRESH = float(args.threshold)

# Load the model
# ~~~~~~~~~~~~~~

PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"

print("Loading model...", end="")
start_time = time.time()

# Load saved model and build the detection function
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

end_time = time.time()
elapsed_time = end_time - start_time
print("Done! Took {} seconds".format(elapsed_time))

# Load label map data (for plotting)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


category_index = label_map_util.create_category_index_from_labelmap(
    PATH_TO_LABELS, use_display_name=True
)

warnings.filterwarnings("ignore")  # Suppress Matplotlib warnings

# TODO, configurar ubicación


def write_to_file(data):
    """
    csv format
        class, ubicación, tiempo, precision
    data
        {
            label: string
            accuracy: int
        }
    """

    if os.environ.get("UBICACION") is None:
        location = "Ninguna Definida"
    else:
        location = os.environ["UBICACION"]

    if not os.path.isfile("detections.csv"):
        with open("detections.csv", "a") as csvfile:
            createCsv(csvfile, data, location)
            csvfile.close()
            return

    # if previous item is the same label then exit
    with open("detections.csv", "r") as csvfile:
        lines = csvfile.read().splitlines()
        last_line = lines[-1].split(",")
        if last_line[0] == data["label"]:
            return

    with open("detections.csv", "a", newline="") as csvfile:
        fieldnames = ["Clase", "Ubicación", "Hora", "Precision"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(
            {
                "Clase": data["label"],
                "Ubicación": location,
                "Hora": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "Precision": data["accuracy"],
            }
        )


def createCsv(csvfile, data, location):
    fieldnames = ["Clase", "Ubicación", "Hora", "Precision"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow(
        {
            "Clase": data["label"],
            "Ubicación": location,
            "Hora": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "Precision": data["accuracy"],
        }
    )


def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.
    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.
    Args:
      path: the file path to the image
    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    return np.array(Image.open(path))


print("Running inference for Webcam", end="")

# Initialize Webcam
videostream = cv2.VideoCapture(0)
ret = videostream.set(3, 1280)
ret = videostream.set(4, 720)


def runInference():
    while True:

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, frame = videostream.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)
        imH, imW, _ = frame.shape

        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(frame)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # input_tensor = np.expand_dims(image_np, 0)
        detections = detect_fn(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(detections.pop("num_detections"))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections["num_detections"] = num_detections

        # detection_classes should be ints.
        detections["detection_classes"] = detections["detection_classes"].astype(np.int64)

        # SET MIN SCORE THRESH TO MINIMUM THRESHOLD FOR DETECTIONS

        detections["detection_classes"] = detections["detection_classes"].astype(np.int64)
        scores = detections["detection_scores"]
        boxes = detections["detection_boxes"]
        classes = detections["detection_classes"]
        # How many objects it detected on the current frame
        count = 0
        helmet = 0
        glasses = 0
        gloves = 0
        suit = 0
        careta = 0
        for i in range(len(scores)):
            if (scores[i] > MIN_CONF_THRESH) and (scores[i] <= 1.0):  # if found!!!
                # increase count
                count += 1
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1, (boxes[i][0] * imH)))
                xmin = int(max(1, (boxes[i][1] * imW)))
                ymax = int(min(imH, (boxes[i][2] * imH)))
                xmax = int(min(imW, (boxes[i][3] * imW)))

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
                # Draw label
                # Look up object name from "labels" array using class index
                object_name = category_index[int(classes[i])]["name"]
                label = "%s: %d%%" % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                )  # Get font size
                # Make sure not to draw label too close to top of window
                label_ymin = max(ymin, labelSize[1] + 10)
                # Draw white box to put label text in
                cv2.rectangle(
                    frame,
                    (xmin, label_ymin - labelSize[1] - 10),
                    (xmin + labelSize[0], label_ymin + baseLine - 10),
                    (255, 255, 255),
                    cv2.FILLED,
                )
                cv2.putText(
                    frame,
                    label,
                    (xmin, label_ymin - 7),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 0),
                    2,
                )  # Draw label text

                # Aqui es donde se guarda el csv
                write_to_file({"label": object_name, "accuracy": int(scores[i] * 100)})
                if object_name:
                    if object_name == "helmet":
                        helmet += 1
                    if object_name == "glasses":
                        glasses += 1
                    if object_name == "gloves":
                        gloves += 1
                    if object_name == "suit":
                        suit += 1
                    if object_name == "careta":
                        careta += 1
                    # ubi.start("objects", count, helmet, glasses, gloves)
                # ubi.start("Objects", count)

        cv2.putText(
            frame,
            "Objects Detected : " + str(count),
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (70, 235, 52),
            2,
            cv2.LINE_AA,
        )
        cv2.imshow("Objects Detector", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
    print("Done")


# runInference()
