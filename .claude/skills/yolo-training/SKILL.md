---
name: yolo-training
description: 用於執行 YOLO 模型訓練、超參數調整與驗證的標準流程。
---

# YOLO Training Workflow

## Standard Training Command
使用 `ultralytics` 函式庫進行訓練。

```python
from ultralytics import YOLO

# Load model
model = YOLO('yolo11n.pt')  # 或使用 'yolov8n.pt'

# Training
results = model.train(
    data='config/data.yaml',
    epochs=150,
    imgsz=640,
    device=0,
    patience=20,
    project='runs/train',
    name='experiment_name'
)
