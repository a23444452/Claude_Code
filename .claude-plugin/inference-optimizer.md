# Inference Optimizer Plugin

## Description
推論優化器，提升預測速度和準確度的平衡策略。

## Optimization Techniques

### 1. Batch Inference
```python
# 批次處理多張圖片
results = model.predict(images, batch=16)
```

### 2. Confidence Threshold
```python
# 調整閾值過濾低信心預測
results = model.predict(image, conf=0.5)  # 預設 0.25
```

### 3. NMS Threshold
```python
# 調整 NMS 減少重複框
results = model.predict(image, iou=0.5)  # 預設 0.45
```

### 4. Image Size
```python
# 降低解析度加速
results = model.predict(image, imgsz=416)  # 預設 640
```

## Speed vs Accuracy Trade-offs

| imgsz | Speed | Accuracy |
|-------|-------|----------|
| 320 | 快 | 低 |
| 416 | 中快 | 中 |
| 640 | 中 | 高 |
| 1280 | 慢 | 最高 |

## Version History
- v1.0.0: 初始版本
