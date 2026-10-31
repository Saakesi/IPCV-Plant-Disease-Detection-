# 🌿 Plant Disease Detection Using YOLOv8

## 1. Project Overview

Plant Disease Detection is a computer vision project that detects plant diseases from leaf images using the YOLOv8 object detection model.

The system identifies diseased regions in an image, predicts the corresponding disease class, and draws bounding boxes around the detected regions.

The project uses the **PlantDoc dataset** and applies transfer learning with the pretrained YOLOv8 Nano (`yolov8n.pt`) model.

## 2. Objectives

- Detect diseases in plant leaf images.
- Identify the disease category of detected regions.
- Localize diseased regions using bounding boxes.
- Train an object detection model using a custom dataset.
- Evaluate model performance using precision, recall, and mAP.

## 3. Technologies Used

- **Python** – Programming language
- **YOLOv8 (Ultralytics)** – Object detection model
- **PyTorch** – Deep learning framework
- **OpenCV** – Image processing
- **Pandas** – Dataset and annotation handling
- **NumPy** – Numerical operations
- **Pillow** – Image processing
- **Apple Metal (MPS)** – Hardware acceleration on Apple Silicon

## 4. Dataset

The project uses the **PlantDoc dataset**, which contains images of healthy and diseased plant leaves.

| Dataset Property | Details |
|---|---|
| Original dataset images | 2,585 |
| Classes | 29 |
| Plant species | 13 |
| Total annotations | 8,600 |
| Training images | 1,800 |
| Validation images | 450 |
| Testing images | 231 |

**Note:** The prepared train, validation, and test splits contain 2,481 images in total. This differs from the original dataset count of 2,585 images.

### Dataset Classes

The dataset contains 29 classes, including:

- Apple Scab Leaf
- Apple Leaf
- Apple Rust Leaf
- Bell Pepper Leaf
- Bell Pepper Leaf Spot
- Blueberry Leaf
- Cherry Leaf
- Corn Gray Leaf Spot
- Corn Leaf Blight
- Corn Rust Leaf
- Peach Leaf
- Potato Leaf
- Potato Leaf Early Blight
- Potato Leaf Late Blight
- Raspberry Leaf
- Soyabean Leaf
- Squash Powdery Mildew Leaf
- Strawberry Leaf
- Tomato Early Blight Leaf
- Tomato Septoria Leaf Spot
- Tomato Leaf
- Tomato Leaf Bacterial Spot
- Tomato Leaf Late Blight
- Tomato Leaf Mosaic Virus
- Tomato Leaf Yellow Virus
- Tomato Mold Leaf
- Tomato Two Spotted Spider Mites Leaf
- Grape Leaf
- Grape Leaf Black Rot

## 5. Project Workflow

1. **Dataset Collection:** Collected plant leaf images from the PlantDoc dataset.
2. **Dataset Organization:** Organized images and their corresponding annotations.
3. **Annotation Processing:** Processed the original CSV annotations.
4. **COCO Conversion:** Converted annotations into COCO JSON format.
5. **YOLO Conversion:** Converted COCO bounding boxes into YOLO annotation format.
6. **Dataset Splitting:** Prepared training, validation, and testing datasets.
7. **Model Selection:** Selected the pretrained YOLOv8 Nano model.
8. **Transfer Learning:** Fine-tuned the pretrained model on the PlantDoc dataset.
9. **Model Evaluation:** Evaluated the model using validation metrics.
10. **Prediction:** Used the trained model to detect diseases in new leaf images.

## 6. Dataset Preprocessing

The original dataset annotations were converted into formats suitable for YOLOv8 training.

### Annotation Conversion Pipeline

```text
Original PlantDoc Dataset
          |
          v
     CSV Annotations
          |
          v
      COCO JSON
          |
          v
      YOLO Format
          |
          v
    Model Training
```

### YOLO Annotation Format

YOLO uses the following annotation format:

```text
class_id x_center y_center width height
```

All bounding box coordinates are normalized between 0 and 1.

- `class_id` – Numeric ID representing the disease class.
- `x_center` – Normalized horizontal center of the bounding box.
- `y_center` – Normalized vertical center of the bounding box.
- `width` – Normalized bounding box width.
- `height` – Normalized bounding box height.

## 7. Model Architecture

The project uses **YOLOv8 Nano (YOLOv8n)**, a lightweight object detection model.

YOLOv8 follows a CNN-based architecture consisting of three major components:

### 1. Backbone

- Extracts important visual features from input images.
- Learns patterns such as edges, textures, shapes, and disease spots.

### 2. Neck

- Combines features from different image scales.
- Helps detect objects of different sizes.

### 3. Detection Head

- Predicts bounding box coordinates.
- Predicts class probabilities.
- Produces the final disease detection results.

### Model Selection

- Model: YOLOv8 Nano
- Pretrained weights: `yolov8n.pt`
- Task: Object Detection
- Input image size: 416 × 416
- Number of classes: 29

## 8. Model Training

Transfer learning was used to train the model.

Instead of training the entire network from scratch, the project starts with pretrained YOLOv8 weights and fine-tunes the model on the PlantDoc dataset.

### Training Configuration

| Parameter | Value |
|---|---|
| Model | YOLOv8n |
| Epochs | 30 |
| Image Size | 416 × 416 |
| Batch Size | 4 |
| Device | MPS |
| Dataset | PlantDoc |
| Task | Object Detection |

### Training Command

```bash
.venv/bin/yolo detect train \
  model=yolov8n.pt \
  data=plantdoc_yolo/data.yaml \
  epochs=30 \
  imgsz=416 \
  batch=4 \
  device=mps \
  workers=0
```

### Training Process

During training:

1. Images are loaded in batches.
2. The model extracts image features.
3. The detection head predicts bounding boxes and classes.
4. Predictions are compared with the actual annotations.
5. The loss is calculated.
6. Backpropagation calculates gradients.
7. The optimizer updates model weights.
8. The process repeats for the specified number of epochs.

### Loss Functions

YOLOv8 uses multiple loss components:

- **Box Loss:** Measures the difference between predicted and actual bounding boxes.
- **Classification Loss:** Measures errors in predicted disease classes.
- **Distribution Focal Loss (DFL):** Helps improve bounding box localization.

## 9. Model Evaluation

The model was evaluated using the validation dataset.

### Validation Results

| Metric | Score |
|---|---:|
| Precision | 0.792 |
| Recall | 0.675 |
| mAP@50 | 0.751 |
| mAP@50–95 | 0.541 |

### Evaluation Metrics Explained

- **Precision:** Measures how many predicted detections are correct.
- **Recall:** Measures how many actual objects are successfully detected.
- **mAP@50:** Mean Average Precision calculated using an Intersection over Union (IoU) threshold of 0.50.
- **mAP@50–95:** Evaluates detection performance across IoU thresholds from 0.50 to 0.95.

## 10. Model Prediction

The trained model can be used to detect diseases in new plant leaf images.

### Prediction Command

```bash
.venv/bin/yolo detect predict \
  model=runs/detect/train/weights/best.pt \
  source=path/to/leaf_image.jpg \
  imgsz=416 \
  conf=0.25 \
  save=True
```

### Prediction Parameters

- `model` – Path to the trained model weights.
- `source` – Input image or video.
- `imgsz` – Input image size.
- `conf` – Minimum confidence threshold for detections.
- `save=True` – Saves the output image with detected bounding boxes.

### Model Weights

- `best.pt` – Model checkpoint with the best validation performance.
- `last.pt` – Model checkpoint saved at the end of training.

## 11. Project Structure

```text
Plant-Disease-Detection/
│
├── plant_diseases/
│   ├── images/
│   ├── csv/
│   ├── labelmap.json
│   └── sets/
│       ├── train.txt
│       ├── val.txt
│       ├── test.txt
│       ├── all.txt
│       └── train_val.txt
│
├── annotations/
│   ├── plant_diseases_instances_train.json
│   ├── plant_diseases_instances_val.json
│   └── plant_diseases_instances_test.json
│
├── scripts/
│   ├── convert_to_coco.py
│   ├── reorganize_dataset.py
│   └── update_csv_labels.py
│
├── plantdoc_yolo/
│   ├── images/
│   ├── labels/
│   └── data.yaml
│
├── runs/
│   └── detect/
│       └── train/
│           └── weights/
│               ├── best.pt
│               └── last.pt
│
├── requirements.txt
└── README.md
```

## 12. Limitations

- The model's validation performance is moderate.
- Similar-looking plant diseases can be difficult to distinguish.
- Performance depends on image quality, lighting, and dataset diversity.
- The model may struggle with leaf images containing complex backgrounds.
- More training data and hyperparameter tuning may improve performance.

## 13. Future Improvements

- Increase the size and diversity of the training dataset.
- Experiment with larger YOLOv8 models.
- Perform data augmentation to improve generalization.
- Tune learning rate, batch size, and other hyperparameters.
- Evaluate performance on additional unseen plant images.
- Develop a web-based interface for uploading leaf images and displaying predictions.

## 14. Conclusion

This project demonstrates the application of deep learning and computer vision for automated plant disease detection.

Using YOLOv8 and transfer learning, the system detects diseased regions in plant leaf images and classifies them into disease categories.

The project also demonstrates the complete object detection pipeline, including dataset preprocessing, annotation conversion, model training, validation, and prediction.

## 15. References

- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [PlantDoc Dataset](https://github.com/pratikkayal/PlantDoc-Dataset)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [OpenCV Documentation](https://docs.opencv.org/)
