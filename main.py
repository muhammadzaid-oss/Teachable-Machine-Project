"""
======================================================
  Teachable Machine - FastAPI Backend (main.py)
  Milestones: Image Ingestion | Training | Inference
======================================================
"""

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import uuid
import pickle
import shutil
import logging
from pathlib import Path
from typing import List

import numpy as np
from PIL import Image
import io

import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# ─────────────────────────────────────────
#  NEXT LEVEL: Professional Logging Setup
# ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("TeachableMachineAPI")

# ─────────────────────────────────────────
#  App Initialization
# ─────────────────────────────────────────
app = FastAPI(
    title="Teachable Machine API",
    description="FastAPI backend for custom image classification using Transfer Learning.",
    version="1.0.0",
)

# ─────────────────────────────────────────
#  Constants / Paths
# ─────────────────────────────────────────
DATASET_DIR = Path("dataset")          # Root folder for all class images
MODEL_PATH  = Path("model.pkl")        # Where trained model bundle is saved

DATASET_DIR.mkdir(exist_ok=True)       # Create dataset folder if it doesn't exist

# ─────────────────────────────────────────
#  PyTorch MobileNetV3 Feature Extractor
# ─────────────────────────────────────────
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"🚀 Initializing AI Backbone on device: {DEVICE}")

# Load pre-trained MobileNetV3-Small as a frozen feature extractor
_weights   = MobileNet_V3_Small_Weights.DEFAULT
_backbone  = mobilenet_v3_small(weights=_weights)
_backbone.classifier = torch.nn.Identity()   # Remove the final classification head
_backbone.eval()
_backbone.to(DEVICE)

# Standard ImageNet preprocessing (must be IDENTICAL in train & predict)
TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],   # ImageNet channel means
        std =[0.229, 0.224, 0.225],   # ImageNet channel stds
    ),
])


# ─────────────────────────────────────────
#  Helper: Extract features from one image
# ─────────────────────────────────────────
def extract_features(pil_image: Image.Image) -> np.ndarray:
    """
    Convert a PIL image → PyTorch tensor → MobileNetV3 feature vector.
    """
    img_rgb = pil_image.convert("RGB")       # Ensure 3-channel input
    tensor  = TRANSFORM(img_rgb).unsqueeze(0).to(DEVICE)   # Add batch dim

    with torch.no_grad():
        features = _backbone(tensor)         # Shape: (1, 576)

    return features.squeeze(0).cpu().numpy()  # Shape: (576,)


# ═══════════════════════════════════════════════════════════════
#  MILESTONE 1 — /upload-sample
# ═══════════════════════════════════════════════════════════════
@app.post("/upload-sample", summary="Upload training images for a class")
async def upload_sample(
    class_name: str              = Form(..., description="Label/category name for these images"),
    files:      List[UploadFile] = File(..., description="One or more image files"),
):
    safe_class = class_name.strip().replace(" ", "_")
    if not safe_class:
        logger.warning("❌ Upload rejected: empty class name received.")
        raise HTTPException(status_code=400, detail="class_name cannot be empty.")

    class_dir = DATASET_DIR / safe_class
    class_dir.mkdir(parents=True, exist_ok=True)

    saved_count = 0
    errors      = []

    for upload in files:
        try:
            contents = await upload.read()
            Image.open(io.BytesIO(contents)).verify()
            ext       = Path(upload.filename).suffix or ".jpg"
            filename  = f"{uuid.uuid4().hex}{ext}"
            save_path = class_dir / filename
            with open(save_path, "wb") as f:
                f.write(contents)
            saved_count += 1
        except Exception as e:
            logger.error(f"⚠️ Corrupt file skipped: {upload.filename}. Error: {str(e)}")
            errors.append(f"{upload.filename}: {str(e)}")

    logger.info(f"💾 Saved {saved_count} new images for class '{safe_class}'.")
    return JSONResponse({
        "status":      "success",
        "class":       safe_class,
        "saved":       saved_count,
        "class_path":  str(class_dir),
        "errors":      errors,
    })


# ═══════════════════════════════════════════════════════════════
#  MILESTONE 2 — /train
# ═══════════════════════════════════════════════════════════════
@app.post("/train", summary="Train the classifier on uploaded images")
async def train_model():
    logger.info("🧠 Model training engine triggered by client request.")
    class_dirs = [d for d in DATASET_DIR.iterdir() if d.is_dir()]

    if len(class_dirs) < 2:
        logger.warning(f"🛑 Training failed: Minimum 2 classes required, only found {len(class_dirs)}.")
        raise HTTPException(
            status_code=400,
            detail=(
                f"Training requires at least 2 class folders. "
                f"Currently found: {len(class_dirs)}. "
                "Please upload images for more classes first."
            ),
        )

    feature_list = []
    label_list   = []
    IMAGE_EXTS   = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for class_dir in sorted(class_dirs):
        image_files = [
            p for p in class_dir.iterdir()
            if p.suffix.lower() in IMAGE_EXTS
        ]

        if len(image_files) == 0:
            logger.warning(f"⚠️ Found empty class folder: '{class_dir.name}'. Training stopped.")
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Class folder '{class_dir.name}' contains no valid images. "
                    "Please upload at least one image per class."
                ),
            )

        for img_path in image_files:
            try:
                pil_img  = Image.open(img_path)
                features = extract_features(pil_img)
                feature_list.append(features)
                label_list.append(class_dir.name)
            except Exception as e:
                logger.error(f"Skipping corrupt image in dataset {img_path}: {str(e)}")
                continue

    if len(feature_list) == 0:
        logger.error("🛑 Dataset is empty or completely unreadable.")
        raise HTTPException(
            status_code=400,
            detail="No valid images could be processed. Please re-upload your dataset.",
        )

    X = np.array(feature_list)
    y = np.array(label_list)

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # FIXED: Logistic Regression configuration
    clf = LogisticRegression(max_iter=1000, C=1.0, solver="lbfgs")
    clf.fit(X, y_encoded)

    model_bundle = {"classifier": clf, "label_encoder": le}
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model_bundle, f)

    logger.info(f"✨ Success! Training finished. Saved bundle to {MODEL_PATH} ({len(feature_list)} samples processed).")
    return JSONResponse({
        "status":        "success",
        "classes":       list(le.classes_),
        "total_samples": len(feature_list),
        "model_saved":   str(MODEL_PATH),
    })


# ═══════════════════════════════════════════════════════════════
#  MILESTONE 3 — /predict
# ═══════════════════════════════════════════════════════════════
@app.post("/predict", summary="Predict the class of a single image")
async def predict(file: UploadFile = File(..., description="Image to classify")):
    if not MODEL_PATH.exists():
        logger.warning("⚠️ Prediction rejected: model.pkl not found. App must be trained first.")
        raise HTTPException(
            status_code=400,
            detail="No trained model found. Please run /train first.",
        )

    with open(MODEL_PATH, "rb") as f:
        bundle = pickle.load(f)

    clf: LogisticRegression = bundle["classifier"]
    le:  LabelEncoder       = bundle["label_encoder"]

    try:
        contents = await file.read()
        pil_img  = Image.open(io.BytesIO(contents))
        features = extract_features(pil_img)
    except Exception as e:
        logger.error(f"❌ Feature extraction failed for inference image: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Could not process image: {str(e)}")

    proba_array = clf.predict_proba([features])[0]
    pred_index  = int(np.argmax(proba_array))
    pred_label  = le.inverse_transform([pred_index])[0]

    all_scores = {
        le.inverse_transform([i])[0]: round(float(p) * 100, 2)
        for i, p in enumerate(proba_array)
    }

    logger.info(f"🎯 Prediction successful: -> {pred_label} ({round(float(proba_array[pred_index]) * 100, 2)}%)")
    return JSONResponse({
        "predicted_class": pred_label,
        "confidence":      round(float(proba_array[pred_index]) * 100, 2),
        "all_scores":      all_scores,
    })


# ─────────────────────────────────────────
#  Health Check
# ─────────────────────────────────────────
@app.get("/", summary="Health check")
def root():
    return {"status": "Teachable Machine API is running smoothly 🚀"}


@app.get("/classes", summary="List all dataset classes and image counts")
def list_classes():
    IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    result = {}
    if DATASET_DIR.exists():
        for d in sorted(DATASET_DIR.iterdir()):
            if d.is_dir():
                count = len([p for p in d.iterdir() if p.suffix.lower() in IMAGE_EXTS])
                result[d.name] = count
    return {"classes": result, "model_trained": MODEL_PATH.exists()}