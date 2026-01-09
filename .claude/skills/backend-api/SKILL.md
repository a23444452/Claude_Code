---
name: backend-api
description: FastAPI 後端開發規範，包含 YOLO 推論 (Inference) 實作。
---

# Backend API Standards

## Setup
使用 `uvicorn main:app --reload` 啟動伺服器。

## Inference Implementation
```python
from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI()
model = YOLO("models/best.pt")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    
    # Inference
    results = model(image)
    
    # Process results (Export to JSON friendly format)
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls),
                "conf": float(box.conf),
                "bbox": box.xywh.tolist()
            })
            
    return {"filename": file.filename, "detections": detections}
```
