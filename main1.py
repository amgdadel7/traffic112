##### Author - Nilesh Chopda

##### Project - Traffic Light Detection and Color Recognition using Tensorflow Object Detection API

### Import Important Libraries

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import gc  # Garbage collection for memory management
import numpy as np
import tarfile
import tensorflow as tf
from matplotlib import pyplot as plt
from PIL import Image
from os import path
from utils import label_map_util
from utils import visualization_utils as vis_util
import time
import cv2
import io
import base64
import threading
import traceback
import urllib.request
from pydantic import BaseModel

app = FastAPI(
    title="Traffic Light Detection API",
    description="API for detecting traffic lights and determining Go/Stop commands",
    version="1.0.0"
)

# Mount static files if موجودة
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic Models
class Base64ImageRequest(BaseModel):
    image_base64: str
    image_format: str = "jpeg"

class DetectionResponse(BaseModel):
    command: str
    confidence: float
    traffic_light_detected: bool
    message: str

# Globals
detection_graph = None
sess = None
category_index = None
MODEL_LOADED = False
MODEL_LOADING_ERROR = None


### Function To Detect Red and Yellow Color
# Here,we are detecting only Red and Yellow colors for the traffic lights as we need to stop the car when it detects these colors.

def detect_red_and_yellow(img, Threshold=0.01):
    """
    detect red and yellow
    :param img:
    :param Threshold:
    :return:
    """

    desired_dim = (30, 90)  # width, height
    img = cv2.resize(np.array(img), desired_dim, interpolation=cv2.INTER_LINEAR)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # lower mask (0-10)
    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red1 = np.array([170, 70, 50])
    upper_red1 = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

    # defining the Range of yellow color
    lower_yellow = np.array([21, 39, 64])
    upper_yellow = np.array([40, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

    # red pixels' mask
    mask = mask0 + mask1 + mask2

    # Compare the percentage of red values
    rate = np.count_nonzero(mask) / (desired_dim[0] * desired_dim[1])

    if rate > Threshold:
        return True
    else:
        return False



### Loading Image Into Numpy Array

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

### Convert Base64 to Image

def base64_to_image(base64_string: str, image_format: str = "jpeg") -> Image.Image:
    """
    Convert base64 string to PIL Image.
    """
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB only if necessary for TensorFlow compatibility
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    return image


### Read Traffic Light objects
# Here,we will write a function to detect TL objects and crop this part of the image to recognize color inside the object. We will create a stop flag,which we will use to take the actions based on recognized color of the traffic light.

def read_traffic_lights_object(image, boxes, scores, classes, max_boxes_to_draw=20, min_score_thresh=0.5,
                               traffic_ligth_label=10):
    im_width, im_height = image.size
    stop_flag = False
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores[i] > min_score_thresh and classes[i] == traffic_ligth_label:
            ymin, xmin, ymax, xmax = tuple(boxes[i].tolist())
            (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                          ymin * im_height, ymax * im_height)
            # guard bounds
            left, right = max(0, int(left)), min(im_width, int(right))
            top, bottom = max(0, int(top)), min(im_height, int(bottom))
            if right <= left or bottom <= top:
                continue
            crop_img = image.crop((left, top, right, bottom))

            if detect_red_and_yellow(crop_img):
                stop_flag = True

    return stop_flag


### Function to Plot detected image

def plot_origin_image(image_np, boxes, classes, scores, category_index):
    # Size of the output images.
    IMAGE_SIZE = (12, 8)
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        min_score_thresh=.5,
        use_normalized_coordinates=True,
        line_thickness=3)
    plt.figure(figsize=IMAGE_SIZE)
    plt.imshow(image_np)

    # save augmented images into hard drive
    # plt.savefig( 'output_images/ouput_' + str(idx) +'.png')
    plt.show()


### Function to Detect Traffic Lights and to Recognize Color

def detect_traffic_lights(PATH_TO_TEST_IMAGES_DIR, MODEL_NAME, Num_images, plot_flag=False):
    """
    Detect traffic lights and draw bounding boxes around the traffic lights
    :param PATH_TO_TEST_IMAGES_DIR: testing image directory
    :param MODEL_NAME: name of the model used in the task
    :return: commands: True: go, False: stop
    """

    # --------test images------
    TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'img_{}.jpg'.format(i)) for i in range(1, Num_images + 1)]

    commands = []

    # What model to download
    MODEL_FILE = MODEL_NAME + '.tar.gz'
    DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

    # List of the strings that is used to add correct label for each box.
    PATH_TO_LABELS = 'mscoco_label_map.pbtxt'

    # number of classes for COCO dataset
    NUM_CLASSES = 90

    # --------Download model----------
    if path.isdir(MODEL_NAME) is False:
        opener = urllib.request.URLopener()
        opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
        tar_file = tarfile.open(MODEL_FILE)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, os.getcwd())

    # --------Load a (frozen) Tensorflow model into memory
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    # ---------Loading label map
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            for image_path in TEST_IMAGE_PATHS:
                image = Image.open(image_path)

                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                image_np = load_image_into_numpy_array(image)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                stop_flag = read_traffic_lights_object(image, np.squeeze(boxes), np.squeeze(scores),
                                                       np.squeeze(classes).astype(np.int32))
                if stop_flag:
                    # print('{}: stop'.format(image_path))  # red or yellow
                    commands.append(False)
                    cv2.putText(image_np, 'Stop', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                else:
                    # print('{}: go'.format(image_path))
                    commands.append(True)
                    cv2.putText(image_np, 'Go', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

                # Visualization of the results of a detection.
                if plot_flag:
                    plot_origin_image(image_np, boxes, classes, scores, category_index)

    return commands


### Function to Detect Traffic Lights in Single Image (for API)

def detect_traffic_lights_in_image(image: Image.Image) -> dict:
    global detection_graph, sess, MODEL_LOADED
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail=f"Model not loaded yet. Error: {MODEL_LOADING_ERROR}")
    try:
        image_np = load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        
        with detection_graph.as_default():
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

        boxes_squeezed = np.squeeze(boxes)
        scores_squeezed = np.squeeze(scores)
        classes_squeezed = np.squeeze(classes).astype(np.int32)
        
        stop_flag = read_traffic_lights_object(
            image, boxes_squeezed, scores_squeezed, classes_squeezed
        )
        
        # Determine command based on original logic: True = go, False = stop
        # stop_flag: True = red/yellow detected (stop), False = green or no traffic light (go)
        if stop_flag:
            command = "Stop"
            message = "Traffic light detected: Red or Yellow signal (Stop)"
        else:
            command = "Go"
            message = "Traffic light detected: Green signal or no traffic light (Go)"
        
        # Check if any traffic light was detected (for traffic_light_detected field)
        traffic_light_detected = False
        for i in range(min(20, len(scores_squeezed))):
            if scores_squeezed[i] > 0.5 and classes_squeezed[i] == 10:  # traffic_light_label = 10
                traffic_light_detected = True
                break
        
        confidence = float(np.max(scores_squeezed)) if len(scores_squeezed) > 0 else 0.0
        
        # Clean up memory
        del image_np, image_np_expanded, boxes, scores, classes, num
        gc.collect()  # Force garbage collection to free memory
        
        return {
            "command": command,
            "confidence": confidence,
            "traffic_light_detected": traffic_light_detected,
            "message": message
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

### Load Model Function

def load_model():
    global detection_graph, sess, category_index, MODEL_LOADED, MODEL_LOADING_ERROR
    
    # Retry mechanism for cloud environments
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"🔄 Model loading attempt {attempt + 1}/{max_retries}")
            _load_model_attempt()
            return  # Success, exit the function
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in 10 seconds...")
                time.sleep(10)
            else:
                print(f"💥 All {max_retries} attempts failed")
                MODEL_LOADED = False
                MODEL_LOADING_ERROR = str(e)
                traceback.print_exc()

def _load_model_attempt():
    global detection_graph, sess, category_index, MODEL_LOADED, MODEL_LOADING_ERROR
    try:
        # Using the same model as original code by Nilesh Chopda
        # MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'    # for faster detection but low accuracy
        MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017'  # for improved accuracy
        MODEL_FILE = MODEL_NAME + '.tar.gz'
        DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
        PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
        PATH_TO_LABELS = 'mscoco_label_map.pbtxt'
        NUM_CLASSES = 90

        # Check if model is already available
        if os.path.exists(PATH_TO_CKPT):
            print("✅ Model already available, skipping download...")
        elif not os.path.exists(MODEL_NAME):
            # First, check if local tar.gz file exists
            if os.path.exists(MODEL_FILE):
                print(f"📦 Found local model file: {MODEL_FILE}")
                print("📦 Extracting local model file...")
                tar_file = tarfile.open(MODEL_FILE)
                for file in tar_file.getmembers():
                    file_name = os.path.basename(file.name)
                    if 'frozen_inference_graph.pb' in file_name:
                        tar_file.extract(file, os.getcwd())
                tar_file.close()
                print("✅ Model extracted successfully from local file!")
            else:
                # Download model
                print("📥 Downloading model (this may take a while)...")
                opener = urllib.request.URLopener()
                opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
                print("✅ Model downloaded successfully!")
                
                print("📦 Extracting model...")
                tar_file = tarfile.open(MODEL_FILE)
                for file in tar_file.getmembers():
                    file_name = os.path.basename(file.name)
                    if 'frozen_inference_graph.pb' in file_name:
                        tar_file.extract(file, os.getcwd())
                tar_file.close()
                print("✅ Model extracted successfully!")

        print("🧠 Loading TensorFlow model...")
        detection_graph_local = tf.Graph()
        with detection_graph_local.as_default():
            try:
                od_graph_def = tf.compat.v1.GraphDef()
                with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                    serialized_graph = fid.read()
                    od_graph_def.ParseFromString(serialized_graph)
                    tf.import_graph_def(od_graph_def, name='')
                print("✅ TensorFlow graph loaded successfully!")
            except Exception as e:
                # Fallback for older TensorFlow versions
                try:
                    od_graph_def = tf.GraphDef()
                    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                        serialized_graph = fid.read()
                        od_graph_def.ParseFromString(serialized_graph)
                        tf.import_graph_def(od_graph_def, name='')
                    print("✅ TensorFlow graph loaded successfully (fallback)!")
                except Exception as e2:
                    raise RuntimeError(f"Failed to load frozen graph: {e2}")

        # load label map
        print("📋 Loading label map...")
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        category_index_local = label_map_util.create_category_index(categories)
        print("✅ Label map loaded successfully!")

        print("🔧 Creating TensorFlow session...")
        config = tf.compat.v1.ConfigProto()
        config.allow_soft_placement = True
        config.log_device_placement = False
        sess_local = tf.compat.v1.Session(graph=detection_graph_local, config=config)
        print("✅ TensorFlow session created successfully!")

        # assign to globals only after success
        detection_graph = detection_graph_local
        sess = sess_local
        category_index = category_index_local
        MODEL_LOADED = True
        MODEL_LOADING_ERROR = None
        print("🎉 Model loaded successfully and ready for inference!")
        
        # Force garbage collection to free memory
        gc.collect()
        print("🧹 Performed garbage collection to free memory")
    except Exception as e:
        MODEL_LOADED = False
        MODEL_LOADING_ERROR = str(e)
        traceback.print_exc()
        print(f"❌ Model failed to load: {MODEL_LOADING_ERROR}")

### FastAPI Startup Event

@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Traffic Light Detection API...")
    print(f"📁 Working directory: {os.getcwd()}")
    print("📥 Loading model in background...")
    
    loader = threading.Thread(target=load_model, daemon=True)
    loader.start()
    print("✅ Model loader thread started (loading in background)")
    
    # Wait a bit for initial model loading
    time.sleep(5)
    
    if MODEL_LOADED:
        print("🎉 Model loaded successfully on startup!")
    else:
        print("⏳ Model still loading... (this may take a few minutes)")

### FastAPI Routes

@app.get("/")
async def root():
    return {
        "message": "Traffic Light Detection API",
        "status": "running",
        "model_loaded": MODEL_LOADED,
        "model_error": MODEL_LOADING_ERROR,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if MODEL_LOADED:
        return {
            "status": "healthy",
            "model_loaded": True,
            "message": "API is ready to process requests"
        }
    elif MODEL_LOADING_ERROR:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "error": MODEL_LOADING_ERROR,
            "message": "Model failed to load"
        }
    else:
        return {
            "status": "loading",
            "model_loaded": False,
            "message": "Model is still loading, please wait..."
        }

@app.get("/status")
async def status():
    """Detailed status endpoint"""
    return {
        "api_status": "running",
        "model_loaded": MODEL_LOADED,
        "model_error": MODEL_LOADING_ERROR
    }

@app.post("/detect", response_model=DetectionResponse)
async def detect_traffic_light(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        result = detect_traffic_lights_in_image(image)
        return DetectionResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.post("/detect-base64", response_model=DetectionResponse)
async def detect_traffic_light_base64(request: Base64ImageRequest):
    try:
        image = base64_to_image(request.image_base64, request.image_format)
        result = detect_traffic_lights_in_image(image)
        # Clean up image from memory
        del image
        gc.collect()  # Force garbage collection
        return DetectionResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error processing base64 image: {str(e)}")

@app.post("/detect-url", response_model=DetectionResponse)
async def detect_traffic_light_url(image_url: str):
    try:
        response = urllib.request.urlopen(image_url)
        image_data = response.read()
        image = Image.open(io.BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        result = detect_traffic_lights_in_image(image)
        return DetectionResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error processing image URL: {str(e)}")

### Let's detect Traffic lights in test_images directory (Original functionality preserved)

if __name__ == "__main__":
    # Specify number of images to detect
    Num_images = 17

    # Specify test directory path
    PATH_TO_TEST_IMAGES_DIR = './test_images'

    # Specify downloaded model name
    # MODEL_NAME ='ssd_mobilenet_v1_coco_11_06_2017'    # for faster detection but low accuracy
    MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017'  # for improved accuracy

    commands = detect_traffic_lights(PATH_TO_TEST_IMAGES_DIR, MODEL_NAME, Num_images, plot_flag=True)
    print(commands)  # commands to print action type, for 'Go' this will return True and for 'Stop' this will return False