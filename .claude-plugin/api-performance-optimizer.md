# API Performance Optimizer Plugin

## Description
FastAPI 效能優化器，分析 YOLO 推論 API 的效能瓶頸，提供快取、批次處理、並發優化等建議。

## Capabilities
- 🚀 推論速度優化
- 💾 快取策略設計
- 📦 批次處理建議
- ⚡ 並發請求優化
- 📊 效能監控和分析
- 🔧 資源使用優化

## When to Use
- API 回應時間過長 (>1s)
- 需要處理高並發請求
- 記憶體使用過高
- CPU/GPU 使用率不理想
- 需要擴展 API 容量

## Key Optimizations

### 1. 模型載入優化
```python
# ❌ 錯誤: 每次請求都載入模型
@app.post("/predict")
async def predict(file: UploadFile):
    model = YOLO("yolo11n.pt")  # 每次都載入！
    results = model.predict(...)

# ✅ 正確: 全域載入一次
model = YOLO("yolo11n.pt")  # 啟動時載入

@app.post("/predict")
async def predict(file: UploadFile):
    results = model.predict(...)  # 直接使用
```

### 2. 批次處理
```python
@app.post("/predict/batch")
async def predict_batch(files: List[UploadFile]):
    images = [await f.read() for f in files]

    # 批次推論（更快）
    results = model.predict(images, batch=len(images))

    return {"detections": [...]}
```

### 3. 非同步處理
```python
from fastapi import BackgroundTasks

@app.post("/predict/async")
async def predict_async(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    # 立即返回任務 ID
    task_id = generate_task_id()

    # 背景處理
    background_tasks.add_task(process_image, task_id, file)

    return {"task_id": task_id, "status": "processing"}
```

### 4. 快取結果
```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_prediction(image_hash: str):
    return model.predict(...)

@app.post("/predict")
async def predict(file: UploadFile):
    content = await file.read()
    img_hash = hashlib.md5(content).hexdigest()

    # 檢查快取
    result = get_cached_prediction(img_hash)
    return result
```

## Performance Targets

- **推論時間**: < 100ms per image
- **API 回應**: < 200ms (包含網路)
- **吞吐量**: > 10 requests/second
- **記憶體**: < 2GB per worker
- **GPU 使用率**: > 70%

## Version History
- v1.0.0: 初始版本
