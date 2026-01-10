# Model Deployment Assistant Plugin

## Description
模型部署助手，協助將 YOLO 模型匯出為不同格式（ONNX, TensorRT, CoreML）並優化以適應目標平台。

## Capabilities
- 📦 多格式匯出 (ONNX, TensorRT, CoreML, TFLite)
- 🔧 模型量化 (INT8, FP16)
- 🚀 推論加速優化
- 📱 邊緣裝置部署指南
- ☁️ 雲端部署最佳實踐
- 🎯 目標平台選擇建議

## Export Formats

### ONNX (通用)
```python
model.export(format='onnx', imgsz=640)
# 用途: 通用格式，跨平台相容
# 優點: 廣泛支援
# 缺點: 速度中等
```

### TensorRT (NVIDIA GPU)
```python
model.export(format='engine', imgsz=640, half=True)
# 用途: NVIDIA GPU 最佳化
# 優點: 最快速度 (2-5x)
# 缺點: 僅 NVIDIA GPU
```

### CoreML (Apple)
```python
model.export(format='coreml', imgsz=640)
# 用途: iOS/macOS 應用
# 優點: Apple 硬體加速
# 缺點: 僅 Apple 平台
```

### TFLite (Mobile)
```python
model.export(format='tflite', imgsz=640, int8=True)
# 用途: Android/嵌入式裝置
# 優點: 小檔案、低功耗
# 缺點: 準確度略降
```

## Quantization

### FP16 (半精度)
- 模型大小: 50% 減少
- 速度: 1.5-2x 提升
- 準確度損失: 極小 (<1%)

### INT8 (8位整數)
- 模型大小: 75% 減少
- 速度: 2-4x 提升
- 準確度損失: 小 (1-3%)

## Deployment Platforms

| 平台 | 推薦格式 | 量化 | 預期速度 |
|------|----------|------|----------|
| NVIDIA GPU | TensorRT | FP16 | 最快 |
| Apple Silicon | CoreML | - | 快 |
| Raspberry Pi | TFLite | INT8 | 中 |
| Cloud CPU | ONNX | - | 中 |
| Android | TFLite | INT8 | 中 |

## Version History
- v1.0.0: 初始版本
