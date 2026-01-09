#!/usr/bin/env python3
"""
FastAPI Backend for YOLO Object Detection
提供圖片上傳和即時物件偵測 API
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import numpy as np
from typing import List, Dict, Any
from pathlib import Path
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 FastAPI
app = FastAPI(
    title="YOLO Detection API",
    description="物件偵測 API - 使用 YOLO 模型進行即時推論",
    version="1.0.0"
)

# CORS 設定（允許前端跨域請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應設定特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全域變數
model = None
MODEL_PATH = "runs/train/exp/weights/best.pt"
CLASS_NAMES = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
    5: '5', 6: '6', 7: '7', 8: '8', 9: '9'
}


@app.on_event("startup")
async def load_model():
    """啟動時載入 YOLO 模型"""
    global model

    model_path = Path(MODEL_PATH)

    if not model_path.exists():
        logger.error(f"找不到模型檔案: {MODEL_PATH}")
        logger.info("請先訓練模型或指定正確的模型路徑")
        # 使用預訓練模型作為備用
        logger.info("使用預訓練模型 yolo11n.pt 作為備用")
        model = YOLO("yolo11n.pt")
    else:
        logger.info(f"載入模型: {MODEL_PATH}")
        model = YOLO(MODEL_PATH)
        logger.info("✓ 模型載入成功")


@app.get("/")
async def root():
    """API 根目錄"""
    return {
        "message": "YOLO Detection API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "model_info": "/model/info"
        }
    }


@app.get("/health")
async def health_check():
    """健康檢查"""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.get("/model/info")
async def model_info():
    """取得模型資訊"""
    if model is None:
        raise HTTPException(status_code=503, detail="模型尚未載入")

    return {
        "model_path": MODEL_PATH,
        "model_type": model.task,
        "classes": CLASS_NAMES,
        "num_classes": len(CLASS_NAMES)
    }


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45
):
    """
    物件偵測 API

    Args:
        file: 上傳的圖片檔案
        conf_threshold: 信心度閾值（預設 0.25）
        iou_threshold: IOU 閾值（預設 0.45）

    Returns:
        偵測結果 JSON
    """
    if model is None:
        raise HTTPException(status_code=503, detail="模型尚未載入")

    # 驗證檔案類型
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"不支援的檔案類型: {file.content_type}，請上傳圖片檔案"
        )

    try:
        # 讀取圖片
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # 確保是 RGB 格式
        if image.mode != 'RGB':
            image = image.convert('RGB')

        logger.info(f"處理圖片: {file.filename}, 尺寸: {image.size}")

        # 執行推論
        results = model(
            image,
            conf=conf_threshold,
            iou=iou_threshold,
            verbose=False
        )

        # 處理結果
        detections = []

        for r in results:
            boxes = r.boxes

            for i in range(len(boxes)):
                box = boxes[i]

                # 取得資訊
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                bbox_xyxy = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                bbox_xywh = box.xywh[0].tolist()  # [center_x, center_y, width, height]

                detection = {
                    "class_id": class_id,
                    "class_name": CLASS_NAMES.get(class_id, f"class_{class_id}"),
                    "confidence": round(confidence, 4),
                    "bbox": {
                        "x1": round(bbox_xyxy[0], 2),
                        "y1": round(bbox_xyxy[1], 2),
                        "x2": round(bbox_xyxy[2], 2),
                        "y2": round(bbox_xyxy[3], 2),
                        "center_x": round(bbox_xywh[0], 2),
                        "center_y": round(bbox_xywh[1], 2),
                        "width": round(bbox_xywh[2], 2),
                        "height": round(bbox_xywh[3], 2)
                    }
                }

                detections.append(detection)

        logger.info(f"偵測到 {len(detections)} 個物件")

        # 回傳結果
        return {
            "success": True,
            "filename": file.filename,
            "image_size": {
                "width": image.size[0],
                "height": image.size[1]
            },
            "detections": detections,
            "detection_count": len(detections),
            "parameters": {
                "conf_threshold": conf_threshold,
                "iou_threshold": iou_threshold
            }
        }

    except Exception as e:
        logger.error(f"推論錯誤: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"推論失敗: {str(e)}"
        )


@app.post("/predict/batch")
async def predict_batch(files: List[UploadFile] = File(...)):
    """
    批次物件偵測 API

    Args:
        files: 多個上傳的圖片檔案

    Returns:
        批次偵測結果
    """
    if model is None:
        raise HTTPException(status_code=503, detail="模型尚未載入")

    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="一次最多上傳 10 張圖片"
        )

    results = []

    for file in files:
        try:
            # 重複使用 predict 的邏輯
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))

            if image.mode != 'RGB':
                image = image.convert('RGB')

            # 執行推論
            detections = []
            model_results = model(image, verbose=False)

            for r in model_results:
                boxes = r.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox_xywh = box.xywh[0].tolist()

                    detections.append({
                        "class_id": class_id,
                        "class_name": CLASS_NAMES.get(class_id, f"class_{class_id}"),
                        "confidence": round(confidence, 4),
                        "bbox": {
                            "center_x": round(bbox_xywh[0], 2),
                            "center_y": round(bbox_xywh[1], 2),
                            "width": round(bbox_xywh[2], 2),
                            "height": round(bbox_xywh[3], 2)
                        }
                    })

            results.append({
                "filename": file.filename,
                "success": True,
                "detections": detections,
                "detection_count": len(detections)
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })

    return {
        "success": True,
        "total_images": len(files),
        "results": results
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
