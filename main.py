# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import gc  # Garbage collection for memory management
import numpy as np
import cv2
from PIL import Image
import io
import base64
import threading
import traceback

# حاول استخدام tf.compat.v1 لتوافق أفضل مع أساليب الـ graph القديمة
import tensorflow as tf
from utils import label_map_util
import urllib.request
import tarfile

from pydantic import BaseModel

app = FastAPI(
    title="Traffic Light Detection API",
    description="API for detecting traffic lights and determining Go/Stop commands",
    version="1.0.0"
)

# Mount static files if موجودة (تجاهل إن لم تكن)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic
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

# Utility functions
def detect_red_and_yellow(img, Threshold=0.01):
    """
    Detect red and yellow colors in traffic light image.
    Based on original implementation by Nilesh Chopda.
    :param img: Image to analyze
    :param Threshold: Threshold for color detection (default 0.01 = 1%)
    :return: True if red/yellow detected, False otherwise
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

def load_image_into_numpy_array(image):
    """
    Load image into numpy array.
    Matching original code behavior - no contrast adjustment, preserves original pixel values.
    """
    (im_width, im_height) = image.size
    # Use same method as original code - preserves original contrast and pixel values
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

def base64_to_image(base64_string: str, image_format: str = "jpeg", max_size: int = None) -> Image.Image:
    """
    Convert base64 string to PIL Image.
    Matching original code behavior - no resizing, no contrast adjustment, no color conversion.
    Image is used exactly as opened, preserving original contrast and colors.
    Only the cropped traffic light region is resized in detect_red_and_yellow.
    """
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB only if necessary for TensorFlow compatibility
    # But preserve original contrast by using the same conversion method as original code
    if image.mode != 'RGB':
        # Use same conversion as original code would do implicitly
        # This preserves contrast better than direct convert('RGB')
        image = image.convert('RGB')
    
    # No resizing - use original image size (matching original code behavior)
    # No contrast adjustment - preserve original contrast
    # The resize only happens in detect_red_and_yellow for the cropped region
    
    return image

# Model related
def read_traffic_lights_object(image, boxes, scores, classes,
                               max_boxes_to_draw=20, min_score_thresh=0.5,
                               traffic_light_label=10):
    """
    Read traffic light objects and detect red/yellow colors.
    Based on original implementation by Nilesh Chopda.
    Creates a stop flag based on recognized color of the traffic light.
    :param image: PIL Image
    :param boxes: Detection boxes
    :param scores: Detection scores
    :param classes: Detection classes
    :param max_boxes_to_draw: Maximum boxes to process
    :param min_score_thresh: Minimum score threshold
    :param traffic_light_label: Label ID for traffic light (10 in COCO)
    :return: stop_flag (True for stop, False for go)
    """
    im_width, im_height = image.size
    stop_flag = False
    
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores[i] > min_score_thresh and classes[i] == traffic_light_label:
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
                import time
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

        # Check if model is already available (pre-built in Docker image)
        if os.path.exists(PATH_TO_CKPT):
            print("✅ Model already available in container (downloaded during build), skipping download...")
            print(f"📁 Model directory contents: {os.listdir(MODEL_NAME) if os.path.exists(MODEL_NAME) else 'Directory not found'}")
        elif not os.path.exists(MODEL_NAME):
            # First, check if local tar.gz file exists
            if os.path.exists(MODEL_FILE):
                print(f"📦 Found local model file: {MODEL_FILE}")
                print("📦 Extracting local model file...")
                # Extract only frozen_inference_graph.pb file (matching original code behavior)
                tar_file = tarfile.open(MODEL_FILE)
                for file in tar_file.getmembers():
                    file_name = os.path.basename(file.name)
                    if 'frozen_inference_graph.pb' in file_name:
                        # Extract to current directory, preserving directory structure
                        tar_file.extract(file, os.getcwd())
                tar_file.close()
                print("✅ Model extracted successfully from local file!")
                
                # Verify model files exist
                if os.path.exists(PATH_TO_CKPT):
                    print(f"✅ Model file verified: {PATH_TO_CKPT}")
                else:
                    print(f"❌ Model file not found: {PATH_TO_CKPT}")
                    raise RuntimeError(f"Model file not found after extraction: {PATH_TO_CKPT}")
            else:
                # Local file doesn't exist, download it
                print("📥 Downloading model (this may take a while)...")
                print(f"📁 Current directory: {os.getcwd()}")
                print(f"📁 Looking for model: {MODEL_NAME}")
                
                # Check if we're in Cloud Run environment
                is_cloud_run = os.environ.get('K_SERVICE') is not None
                if is_cloud_run:
                    print("☁️ Cloud Run environment detected - using optimized download strategy")
                
                # Updated download URLs - TensorFlow has moved model hosting
                DOWNLOAD_URLS = [
                    f'https://storage.googleapis.com/download.tensorflow.org/models/object_detection/{MODEL_FILE}',
                    f'https://github.com/tensorflow/models/raw/master/research/object_detection/test_data/{MODEL_FILE}',
                    f'http://download.tensorflow.org/models/object_detection/{MODEL_FILE}'
                ]
                
                download_success = False
                
                for i, download_url in enumerate(DOWNLOAD_URLS):
                    try:
                        print(f"🌐 Trying download URL {i+1}/{len(DOWNLOAD_URLS)}: {download_url}")
                        # Add timeout and better error handling
                        import urllib.request
                        import urllib.error
                        
                        req = urllib.request.Request(download_url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                        
                        # Longer timeout for Cloud Run
                        timeout = 120 if is_cloud_run else 60
                        with urllib.request.urlopen(req, timeout=timeout) as response:
                            with open(MODEL_FILE, 'wb') as f:
                                # Read in chunks to handle large files better
                                chunk_size = 8192
                                while True:
                                    chunk = response.read(chunk_size)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                        
                        print("✅ Model downloaded successfully!")
                        download_success = True
                        break
                    except Exception as e:
                        print(f"❌ Download failed from URL {i+1}: {str(e)}")
                        if i < len(DOWNLOAD_URLS) - 1:
                            print("🔄 Trying next URL...")
                            # Wait before retry in Cloud Run
                            if is_cloud_run:
                                import time
                                time.sleep(5)
                        continue
                
                if not download_success:
                    raise RuntimeError("All download URLs failed. Please check your internet connection or download the model manually.")
                
                print("📦 Extracting model...")
                # Extract only frozen_inference_graph.pb file (matching original code behavior)
                tar_file = tarfile.open(MODEL_FILE)
                for file in tar_file.getmembers():
                    file_name = os.path.basename(file.name)
                    if 'frozen_inference_graph.pb' in file_name:
                        # Extract to current directory, preserving directory structure
                        tar_file.extract(file, os.getcwd())
                tar_file.close()
                print("✅ Model extracted successfully!")
                
                # Clean up tar file to save space (optional - comment out if you want to keep it)
                # if os.path.exists(MODEL_FILE):
                #     os.remove(MODEL_FILE)
                #     print("🧹 Cleaned up tar file to save space")
                
                # Verify model files exist
                if os.path.exists(PATH_TO_CKPT):
                    print(f"✅ Model file verified: {PATH_TO_CKPT}")
                else:
                    print(f"❌ Model file not found: {PATH_TO_CKPT}")
                    raise RuntimeError(f"Model file not found after extraction: {PATH_TO_CKPT}")
        else:
            print("✅ Model already exists, skipping download...")
            print(f"📁 Model directory contents: {os.listdir(MODEL_NAME) if os.path.exists(MODEL_NAME) else 'Directory not found'}")

        print("🧠 Loading TensorFlow model...")
        detection_graph_local = tf.Graph()
        with detection_graph_local.as_default():
            # for TF 2.x compatibility:
            try:
                od_graph_def = tf.compat.v1.GraphDef()
                with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                    serialized_graph = fid.read()
                    od_graph_def.ParseFromString(serialized_graph)
                    tf.import_graph_def(od_graph_def, name='')
                print("✅ TensorFlow graph loaded successfully!")
                
                # Clear the serialized graph to free memory
                del serialized_graph
                del od_graph_def
                print("🧹 Freed graph loading memory")
            except Exception as e:
                # Fallback for older TensorFlow versions
                try:
                    od_graph_def = tf.GraphDef()
                    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                        serialized_graph = fid.read()
                        od_graph_def.ParseFromString(serialized_graph)
                        tf.import_graph_def(od_graph_def, name='')
                    print("✅ TensorFlow graph loaded successfully (fallback)!")
                    
                    # Clear the serialized graph to free memory
                    del serialized_graph
                    del od_graph_def
                    print("🧹 Freed graph loading memory")
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
        
        # Clear label map data to free memory
        del label_map
        del categories
        print("🧹 Freed label map memory")

        print("🔧 Creating TensorFlow session...")
        # Configure session for better memory management in cloud
        config = tf.compat.v1.ConfigProto()
        config.allow_soft_placement = True
        config.log_device_placement = False
        
        # Check if we're in Cloud Run environment
        is_cloud_run = os.environ.get('K_SERVICE') is not None
        
        if is_cloud_run:
            print("☁️ Cloud Run detected - using optimized configuration")
            # Optimize for Cloud Run (CPU-only, memory efficient)
            config.inter_op_parallelism_threads = 1
            config.intra_op_parallelism_threads = 1
            # Disable XLA JIT compilation to save memory
            config.graph_options.optimizer_options.global_jit_level = tf.compat.v1.OptimizerOptions.OFF
            # Memory optimization
            config.graph_options.rewrite_options.arithmetic_optimization = tf.compat.v1.OptimizerOptions.OFF
            config.graph_options.rewrite_options.constant_folding = tf.compat.v1.OptimizerOptions.OFF
        else:
            # Local development configuration
            config.inter_op_parallelism_threads = 0
            config.intra_op_parallelism_threads = 0
            # Memory optimization for cloud deployment
            config.gpu_options.allow_growth = True
            config.gpu_options.per_process_gpu_memory_fraction = 0.1  # Use only 10% of GPU memory
            # Disable XLA JIT compilation to save memory
            config.graph_options.optimizer_options.global_jit_level = tf.compat.v1.OptimizerOptions.OFF
        
        sess_local = tf.compat.v1.Session(graph=detection_graph_local, config=config)
        print("✅ TensorFlow session created successfully!")
        
        # Skip session test in cloud to save memory
        if is_cloud_run:
            print("⏭️ Skipping session test to save memory in Cloud Run environment")
        else:
            print("⏭️ Skipping session test to save memory")

        # assign to globals only after success
        detection_graph = detection_graph_local
        sess = sess_local
        category_index = category_index_local
        MODEL_LOADED = True
        MODEL_LOADING_ERROR = None
        print("🎉 Model loaded successfully and ready for inference!")
        
        # Force garbage collection to free memory
        import gc
        gc.collect()
        print("🧹 Performed garbage collection to free memory")
    except Exception as e:
        MODEL_LOADED = False
        MODEL_LOADING_ERROR = str(e)
        traceback.print_exc()
        print(f"❌ Model failed to load: {MODEL_LOADING_ERROR}")

# Startup: spawn background loader thread so FastAPI responds immediately
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Traffic Light Detection API...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📁 Files in directory: {os.listdir('.')}")
    print("📥 Loading model in background...")
    
    # Check environment
    is_docker = os.path.exists('/.dockerenv')
    is_cloud_run = os.environ.get('K_SERVICE') is not None
    
    if is_cloud_run:
        print("☁️ Cloud Run environment detected")
        print("⏳ Cloud Run: Model loading may take longer due to network and resource constraints")
    elif is_docker:
        print("🐳 Running in Docker container")
        print("⏳ Docker detected - allowing extra time for model download...")
    
    loader = threading.Thread(target=load_model, daemon=True)
    loader.start()
    print("✅ Model loader thread started (loading in background)")
    
    # Wait a bit for initial model loading based on environment
    import time
    if is_cloud_run:
        wait_time = 30  # More time for Cloud Run
    elif is_docker:
        wait_time = 15  # Medium time for Docker
    else:
        wait_time = 5   # Short time for local
    
    print(f"⏳ Waiting {wait_time} seconds for initial model loading...")
    time.sleep(wait_time)
    
    # Check if model loaded successfully
    if MODEL_LOADED:
        print("🎉 Model loaded successfully on startup!")
    else:
        print("⏳ Model still loading... (this may take a few minutes)")
        if is_cloud_run:
            print("☁️ Cloud Run: Model download and loading may take 2-5 minutes")
        elif is_docker:
            print("🐳 Docker: Model download may take longer due to network constraints")

# Routes
@app.get("/")
async def root():
    return {
        "message": "Traffic Light Detection API",
        "status": "running",
        "model_loaded": MODEL_LOADED,
        "model_error": MODEL_LOADING_ERROR,
        "docs": "/docs",
        "web_interface": "/static/index.html" if os.path.isdir("static") else None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
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
    is_cloud_run = os.environ.get('K_SERVICE') is not None
    is_docker = os.path.exists('/.dockerenv')
    
    return {
        "api_status": "running",
        "model_loaded": MODEL_LOADED,
        "model_error": MODEL_LOADING_ERROR,
        "environment": {
            "cloud_run": is_cloud_run,
            "docker": is_docker,
            "service_name": os.environ.get('K_SERVICE', 'N/A')
        },
        "memory_info": {
            "available": "N/A"  # Could add memory monitoring here
        }
    }


@app.get("/model-status")
async def model_status():
    """Detailed model loading status"""
    return {
        "model_loaded": MODEL_LOADED,
        "model_error": MODEL_LOADING_ERROR,
        "status": "ready" if MODEL_LOADED else "loading" if MODEL_LOADING_ERROR is None else "error",
        "message": "Model is ready for inference" if MODEL_LOADED else 
                  "Model is still loading, please wait..." if MODEL_LOADING_ERROR is None else 
                  f"Model failed to load: {MODEL_LOADING_ERROR}"
    }

@app.post("/reload-model")
async def reload_model():
    """Manually reload the model"""
    global MODEL_LOADED, MODEL_LOADING_ERROR
    
    if MODEL_LOADED:
        return {"message": "Model is already loaded", "status": "success"}
    
    try:
        print("🔄 Manual model reload requested...")
        MODEL_LOADED = False
        MODEL_LOADING_ERROR = None
        
        # Start model loading in background
        loader = threading.Thread(target=load_model, daemon=True)
        loader.start()
        
        return {
            "message": "Model reload started in background", 
            "status": "loading",
            "note": "Check /model-status endpoint for progress"
        }
    except Exception as e:
        return {
            "message": f"Failed to start model reload: {str(e)}", 
            "status": "error"
        }

@app.post("/detect", response_model=DetectionResponse)
async def detect_traffic_light(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Open image exactly as original code - no preprocessing, preserves contrast
        image = Image.open(io.BytesIO(contents))
        # Convert to RGB only if necessary (for TensorFlow compatibility)
        # This preserves original contrast
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
        # Use original image size (matching original code behavior)
        image = base64_to_image(request.image_base64, request.image_format, max_size=None)
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
        # Open image exactly as original code - no preprocessing, preserves contrast
        image = Image.open(io.BytesIO(image_data))
        # Convert to RGB only if necessary (for TensorFlow compatibility)
        # This preserves original contrast
        if image.mode != 'RGB':
            image = image.convert('RGB')
        result = detect_traffic_lights_in_image(image)
        return DetectionResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Error processing image URL: {str(e)}")

### Import Important Libraries

# import numpy as np
# import os
# import six.moves.urllib as urllib
# import tarfile
# import tensorflow as tf
# from matplotlib import pyplot as plt
# from PIL import Image
# from os import path
# from utils import label_map_util
# from utils import visualization_utils as vis_util
# import time
# import cv2

# def detect_red_and_yellow(img, Threshold=0.01):
#     """
#     detect red and yellow
#     :param img:
#     :param Threshold:
#     :return:
#     """

#     desired_dim = (30, 90)  # width, height
#     img = cv2.resize(np.array(img), desired_dim, interpolation=cv2.INTER_LINEAR)
#     img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

#     # lower mask (0-10)
#     lower_red = np.array([0, 70, 50])
#     upper_red = np.array([10, 255, 255])
#     mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

#     # upper mask (170-180)
#     lower_red1 = np.array([170, 70, 50])
#     upper_red1 = np.array([180, 255, 255])
#     mask1 = cv2.inRange(img_hsv, lower_red1, upper_red1)

#     # defining the Range of yellow color
#     lower_yellow = np.array([21, 39, 64])
#     upper_yellow = np.array([40, 255, 255])
#     mask2 = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

#     # red pixels' mask
#     mask = mask0 + mask1 + mask2

#     # Compare the percentage of red values
#     rate = np.count_nonzero(mask) / (desired_dim[0] * desired_dim[1])

#     if rate > Threshold:
#         return True
#     else:
#         return False
# def load_image_into_numpy_array(image):
#     (im_width, im_height) = image.size
#     return np.array(image.getdata()).reshape(
#         (im_height, im_width, 3)).astype(np.uint8)
# def plot_origin_image(image_np, boxes, classes, scores, category_index):
#     # Size of the output images.
#     IMAGE_SIZE = (12, 8)
#     vis_util.visualize_boxes_and_labels_on_image_array(
#         image_np,
#         np.squeeze(boxes),
#         np.squeeze(classes).astype(np.int32),
#         np.squeeze(scores),
#         category_index,
#         min_score_thresh=.5,
#         use_normalized_coordinates=True,
#         line_thickness=3)
#     plt.figure(figsize=IMAGE_SIZE)
#     plt.imshow(image_np)

#     # save augmented images into hard drive
#     # plt.savefig( 'output_images/ouput_' + str(idx) +'.png')
#     plt.show()
# def detect_traffic_lights(PATH_TO_TEST_IMAGES_DIR, MODEL_NAME, Num_images, plot_flag=False):
#     """
#     Detect traffic lights and draw bounding boxes around the traffic lights
#     :param PATH_TO_TEST_IMAGES_DIR: testing image directory
#     :param MODEL_NAME: name of the model used in the task
#     :return: commands: True: go, False: stop
#     """

#     # --------test images------
#     TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'img_{}.jpg'.format(i)) for i in range(1, Num_images + 1)]

#     commands = []

#     # What model to download
#     MODEL_FILE = MODEL_NAME + '.tar.gz'
#     DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

#     # Path to frozen detection graph. This is the actual model that is used for the object detection.
#     PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

#     # List of the strings that is used to add correct label for each box.
#     PATH_TO_LABELS = 'mscoco_label_map.pbtxt'

#     # number of classes for COCO dataset
#     NUM_CLASSES = 90

#     # --------Download model----------
#     if path.isdir(MODEL_NAME) is False:
#         opener = urllib.request.URLopener()
#         opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#         tar_file = tarfile.open(MODEL_FILE)
#         for file in tar_file.getmembers():
#             file_name = os.path.basename(file.name)
#             if 'frozen_inference_graph.pb' in file_name:
#                 tar_file.extract(file, os.getcwd())

#     # --------Load a (frozen) Tensorflow model into memory
#     detection_graph = tf.Graph()
#     with detection_graph.as_default():
#         od_graph_def = tf.GraphDef()
#         with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
#             serialized_graph = fid.read()
#             od_graph_def.ParseFromString(serialized_graph)
#             tf.import_graph_def(od_graph_def, name='')

#     # ---------Loading label map
#     label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
#     categories = label_map_util.convert_label_map_to_categories(label_map,
#                                                                 max_num_classes=NUM_CLASSES,
#                                                                 use_display_name=True)
#     category_index = label_map_util.create_category_index(categories)

#     with detection_graph.as_default():
#         with tf.Session(graph=detection_graph) as sess:
#             # Definite input and output Tensors for detection_graph
#             image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
#             # Each box represents a part of the image where a particular object was detected.
#             detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
#             # Each score represent how level of confidence for each of the objects.
#             # Score is shown on the result image, together with the class label.
#             detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
#             detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
#             num_detections = detection_graph.get_tensor_by_name('num_detections:0')

#             for image_path in TEST_IMAGE_PATHS:
#                 image = Image.open(image_path)

#                 # the array based representation of the image will be used later in order to prepare the
#                 # result image with boxes and labels on it.
#                 image_np = load_image_into_numpy_array(image)
#                 # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
#                 image_np_expanded = np.expand_dims(image_np, axis=0)
#                 # Actual detection.
#                 (boxes, scores, classes, num) = sess.run(
#                     [detection_boxes, detection_scores, detection_classes, num_detections],
#                     feed_dict={image_tensor: image_np_expanded})

#                 stop_flag = read_traffic_lights_object(image, np.squeeze(boxes), np.squeeze(scores),
#                                                        np.squeeze(classes).astype(np.int32))
#                 if stop_flag:
#                     # print('{}: stop'.format(image_path))  # red or yellow
#                     commands.append(False)
#                     cv2.putText(image_np, 'Stop', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
#                 else:
#                     # print('{}: go'.format(image_path))
#                     commands.append(True)
#                     cv2.putText(image_np, 'Go', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

#                 # Visualization of the results of a detection.
#                 if plot_flag:
#                     plot_origin_image(image_np, boxes, classes, scores, category_index)

#     return commands
# if __name__ == "__main__":
#     # Specify number of images to detect
#     Num_images = 5

#     # Specify test directory path
#     PATH_TO_TEST_IMAGES_DIR = './test_images'

#     # Specify downloaded model name
#     # MODEL_NAME ='ssd_mobilenet_v1_coco_11_06_2017'    # for faster detection but low accuracy
#     MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017'  # for improved accuracy

#     commands = detect_traffic_lights(PATH_TO_TEST_IMAGES_DIR, MODEL_NAME, Num_images, plot_flag=True)
#     print(commands)  # commands to print action type, for 'Go' this will return True and for 'Stop' this will return False

