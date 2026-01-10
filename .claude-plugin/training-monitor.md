# Training Monitor Plugin

## Description
即時訓練監控器，追蹤訓練指標、偵測異常並提供即時建議。

## Monitored Metrics
- Loss (train/val)
- mAP@0.5, mAP@0.5:0.95
- Precision, Recall
- Learning rate
- GPU/Memory usage

## Alerts
- 🔴 Loss 爆炸 (>10)
- 🟡 Loss 停滯 (10 epochs 無改善)
- 🟡 過擬合 (train/val gap > 0.3)
- 🔴 記憶體不足
- 🟡 GPU 使用率低 (<30%)

## Usage
```python
# 查看訓練曲線
runs/detect/train/results.png

# 即時日誌
tail -f runs/detect/train/train.log
```

## Version History
- v1.0.0: 初始版本
