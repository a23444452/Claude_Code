# Model Comparison Tool Plugin

## Description
YOLO 模型比較工具，分析不同模型變體的效能差異，推薦最適合的模型。

## Model Variants

| Model | Size | Params | mAP | Speed | Use Case |
|-------|------|--------|-----|-------|----------|
| n | 6MB | 2.6M | 39.5% | 1.5ms | 邊緣裝置 |
| s | 22MB | 9.4M | 47.0% | 2.3ms | 一般應用 |
| m | 50MB | 20.1M | 51.5% | 4.5ms | 平衡選擇 |
| l | 58MB | 25.3M | 53.4% | 6.5ms | 高準確度 |
| x | 138MB | 56.9M | 54.7% | 10.6ms | 最高精度 |

## Selection Guide

### By Hardware
- **Raspberry Pi**: yolo11n
- **CPU Server**: yolo11s
- **GPU Server**: yolo11m/l
- **Mobile**: yolo11n + quantization

### By Requirement
- **Real-time (>30 FPS)**: yolo11n/s
- **Accuracy-first**: yolo11l/x
- **Balanced**: yolo11m

## Comparison Script
```python
for model_name in ['yolo11n', 'yolo11s', 'yolo11m']:
    model = YOLO(f'{model_name}.pt')
    metrics = model.val(data='data.yaml')
    print(f"{model_name}: mAP={metrics.box.map:.3f}")
```

## Version History
- v1.0.0: 初始版本
