# YOLO Detection API

FastAPI 後端服務，提供 YOLO 物件偵測功能。

## 功能

- ✓ 單張圖片偵測
- ✓ 批次圖片偵測（最多 10 張）
- ✓ 可調整信心度和 IOU 閾值
- ✓ 完整的偵測結果（座標、類別、信心度）
- ✓ CORS 支援（跨域請求）
- ✓ 健康檢查和模型資訊查詢

## 啟動服務

### 方法 1: 使用 uvicorn（開發模式）
```bash
cd /Users/vincewang/YOLO_Project
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 方法 2: 直接執行
```bash
cd /Users/vincewang/YOLO_Project
python src/api/main.py
```

啟動後訪問：
- API 文檔（Swagger UI）: http://localhost:8000/docs
- API 文檔（ReDoc）: http://localhost:8000/redoc
- 健康檢查: http://localhost:8000/health

## API Endpoints

### 1. 健康檢查
```bash
GET /health
```

**回應:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 2. 模型資訊
```bash
GET /model/info
```

**回應:**
```json
{
  "model_path": "runs/train/exp/weights/best.pt",
  "model_type": "detect",
  "classes": {"0": "0", "1": "1", ...},
  "num_classes": 10
}
```

### 3. 單張圖片偵測
```bash
POST /predict
Content-Type: multipart/form-data

Parameters:
  - file: 圖片檔案
  - conf_threshold: 信心度閾值（預設 0.25）
  - iou_threshold: IOU 閾值（預設 0.45）
```

**回應:**
```json
{
  "success": true,
  "filename": "test.jpg",
  "image_size": {
    "width": 1280,
    "height": 720
  },
  "detections": [
    {
      "class_id": 0,
      "class_name": "0",
      "confidence": 0.8523,
      "bbox": {
        "x1": 100.5,
        "y1": 200.3,
        "x2": 150.8,
        "y2": 250.1,
        "center_x": 125.65,
        "center_y": 225.2,
        "width": 50.3,
        "height": 49.8
      }
    }
  ],
  "detection_count": 1,
  "parameters": {
    "conf_threshold": 0.25,
    "iou_threshold": 0.45
  }
}
```

### 4. 批次偵測
```bash
POST /predict/batch
Content-Type: multipart/form-data

Parameters:
  - files: 多個圖片檔案（最多 10 張）
```

## 使用範例

### cURL
```bash
# 單張圖片偵測
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test.jpg" \
  -F "conf_threshold=0.3"

# 批次偵測
curl -X POST "http://localhost:8000/predict/batch" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg"
```

### Python
```python
import requests

# 單張圖片偵測
with open('test.jpg', 'rb') as f:
    files = {'file': f}
    params = {'conf_threshold': 0.3}
    response = requests.post(
        'http://localhost:8000/predict',
        files=files,
        params=params
    )
    result = response.json()
    print(f"偵測到 {result['detection_count']} 個物件")
```

### JavaScript (Fetch API)
```javascript
// 單張圖片偵測
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict?conf_threshold=0.3', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('偵測結果:', data.detections);
});
```

## 測試

使用提供的測試腳本：
```bash
python src/api/test_api.py
```

## 注意事項

1. **模型路徑**: 預設使用 `runs/train/exp/weights/best.pt`，請確認模型存在
2. **記憶體**: 載入模型需要記憶體，建議至少 2GB 可用記憶體
3. **CORS**: 預設允許所有來源，生產環境請修改 `allow_origins`
4. **檔案大小**: 建議限制上傳檔案大小（可在 FastAPI 中設定）

## 效能優化

1. 使用 GPU 加速（如果可用）
2. 批次處理多張圖片
3. 調整模型大小（nano/small/medium）
4. 使用快取機制

## 部署

### Docker
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生產環境
```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```
