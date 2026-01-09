# YOLO 物件偵測系統架構

## 系統架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                        使用者                                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   前端 (Port 3000)                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │  index.html - 使用者介面                            │    │
│  │  - 圖片上傳 (拖曳/點擊)                             │    │
│  │  - 參數調整 (信心度/IOU)                            │    │
│  │  - 結果視覺化 (Canvas 繪圖)                         │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  app.js - 核心邏輯                                  │    │
│  │  - Fetch API 通訊                                   │    │
│  │  - Canvas 繪圖                                      │    │
│  │  - 結果處理與顯示                                   │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP POST
                          │ FormData (image)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   後端 API (Port 8000)                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │  FastAPI - REST API                                 │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │  GET  /health       - 健康檢查              │  │    │
│  │  │  GET  /model/info   - 模型資訊              │  │    │
│  │  │  POST /predict      - 單張偵測              │  │    │
│  │  │  POST /predict/batch - 批次偵測             │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────┬───────────────────────────┘    │
│                            │                                 │
│                            ▼                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │  YOLO 模型引擎 (Ultralytics)                        │    │
│  │  - 圖片預處理                                       │    │
│  │  - 模型推論 (MPS 加速)                              │    │
│  │  - 後處理 (NMS)                                     │    │
│  │  - 結果格式化                                       │    │
│  └────────────────────────┬───────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    訓練好的模型                              │
│  runs/train/exp/weights/best.pt                             │
│  - YOLO11n 架構                                              │
│  - 10 類物件                                                 │
│  - MPS 優化                                                  │
└─────────────────────────────────────────────────────────────┘
```

## 資料流程

### 1. 訓練階段

```
原始資料
   ↓
dataset/MBB_gray_dataset/
├── image1.jpg
├── image1.txt (YOLO 格式標註)
└── ...
   ↓
[preprocess.py - 資料預處理]
├── 驗證圖片完整性
├── RGB 轉換
├── 標註驗證
└── train/val 切分
   ↓
dataset/MBB_gray_processed/
├── images/
│   ├── train/ (80%)
│   └── val/   (20%)
└── labels/
    ├── train/
    └── val/
   ↓
[train.py - 模型訓練]
├── 載入 YOLO11n 預訓練模型
├── 資料增強
├── MPS 加速訓練
├── 驗證與早停
└── 保存最佳模型
   ↓
runs/train/exp/weights/best.pt
```

### 2. 推論階段

```
使用者上傳圖片
   ↓
[前端] 封裝為 FormData
   ↓
HTTP POST → /predict
   ↓
[後端 API] 接收請求
   ↓
[PIL] 讀取圖片
   ↓
[YOLO 模型] 推論
├── 預處理 (resize, normalize)
├── 模型前向傳播
└── 後處理 (NMS, 座標轉換)
   ↓
偵測結果 JSON
{
  "detections": [
    {
      "class_id": 0,
      "class_name": "0",
      "confidence": 0.85,
      "bbox": {...}
    }
  ]
}
   ↓
[前端] 接收結果
   ↓
[Canvas] 繪製邊界框
   ↓
顯示給使用者
```

## 技術棧

### 前端
- **HTML5**: 結構
- **CSS3**: 樣式 (Gradient, Grid, Flexbox)
- **JavaScript (ES6+)**: 邏輯
  - Fetch API: HTTP 通訊
  - Canvas API: 圖像繪製
  - File API: 檔案處理
  - Drag & Drop API: 拖曳上傳

### 後端
- **Python 3.10+**: 程式語言
- **FastAPI**: Web 框架
- **Uvicorn**: ASGI 伺服器
- **Ultralytics YOLO**: 物件偵測引擎
- **PyTorch**: 深度學習框架
- **PIL/Pillow**: 圖像處理

### 訓練
- **PyTorch**: 深度學習框架
- **MPS (Metal Performance Shaders)**: Apple Silicon 加速
- **YOLO11n**: 輕量級物件偵測模型
- **Data Augmentation**: 資料增強技術

## 模型規格

### YOLO11n
- **參數量**: 2.59M
- **FLOPs**: 6.5G
- **輸入尺寸**: 640x640
- **類別數**: 10
- **架構**:
  - Backbone: C3k2 + SPPF
  - Neck: C2PSA + PANet
  - Head: Decoupled Head

### 訓練配置
```python
{
    "model": "yolo11n",
    "epochs": 100,
    "batch_size": 8,
    "image_size": 640,
    "device": "mps",
    "optimizer": "AdamW",
    "lr": 0.000714,
    "augmentation": {
        "hsv_h": 0.02,
        "hsv_s": 0.7,
        "hsv_v": 0.4,
        "degrees": 10.0,
        "translate": 0.2,
        "scale": 0.5,
        "flipud": 0.5,
        "fliplr": 0.5,
        "mosaic": 1.0,
        "mixup": 0.1
    }
}
```

## API 規格

### Endpoint 總覽

| Endpoint | 方法 | 功能 | 參數 |
|----------|------|------|------|
| `/health` | GET | 健康檢查 | - |
| `/model/info` | GET | 模型資訊 | - |
| `/predict` | POST | 單張偵測 | file, conf_threshold, iou_threshold |
| `/predict/batch` | POST | 批次偵測 | files[] |

### 請求格式

**單張偵測**
```http
POST /predict?conf_threshold=0.25&iou_threshold=0.45
Content-Type: multipart/form-data

file: [binary image data]
```

### 回應格式

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

## 效能指標

### 訓練效能
- **訓練時間**: ~2秒/epoch (29張訓練圖，batch=8)
- **推論速度**: ~100ms/image (MPS)
- **模型大小**: 5.5MB (best.pt)

### API 效能
- **回應時間**:
  - 640x640 圖片: ~100-200ms
  - 1280x720 圖片: ~150-300ms
- **吞吐量**: ~5-10 請求/秒 (單 worker)
- **記憶體使用**: ~500MB (含模型)

### 前端效能
- **首次載入**: <1s
- **圖片上傳**: 即時
- **結果渲染**: <100ms
- **Canvas 繪製**: <50ms

## 擴展性

### 水平擴展
```bash
# 多個 API worker
uvicorn src.api.main:app --workers 4

# 負載均衡 (Nginx)
upstream api_backend {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}
```

### 垂直擴展
- 使用更大的模型 (s/m/l)
- 增加 batch size
- GPU 加速

### 功能擴展
- [ ] 影片偵測
- [ ] 即時串流
- [ ] 多模型切換
- [ ] 偵測結果儲存
- [ ] 使用者認證
- [ ] 監控儀表板

## 安全性

### API 安全
- CORS 配置
- 檔案大小限制
- 檔案類型驗證
- Rate limiting (建議)
- API Key 認證 (建議)

### 前端安全
- XSS 防護
- CSRF 防護
- 輸入驗證
- HTTPS (生產環境)

## 監控與日誌

### 日誌位置
```
logs/
├── api.log         # API 請求日誌
└── frontend.log    # 前端訪問日誌
```

### 監控指標
- API 請求數
- 平均回應時間
- 錯誤率
- 模型推論時間
- 記憶體使用

## 部署架構

### 開發環境
```
localhost:3000 (前端)
    ↓
localhost:8000 (API)
```

### 生產環境
```
users
  ↓
[Nginx] :80/:443
  ↓
  ├─→ [Frontend] (靜態檔案)
  └─→ [API] :8000
       ↓
    [YOLO Model]
```

## 依賴關係

```
前端
└── 無外部依賴 (純 Vanilla JS)

後端 API
├── fastapi
├── uvicorn
├── python-multipart
├── pillow
└── ultralytics
    ├── torch
    ├── numpy
    └── opencv-python

訓練
├── ultralytics
├── torch
└── pillow
```

## 版本資訊

- Python: 3.10+
- PyTorch: 2.9.1
- Ultralytics: 8.3.240
- FastAPI: 0.104.1
- YOLO: 11n

## 更新日誌

### v1.0.0 (2026-01-09)
- ✅ 完整的資料預處理流程
- ✅ YOLO11n 模型訓練
- ✅ FastAPI 後端 API
- ✅ Web 前端介面
- ✅ MPS 加速支援
- ✅ 完整文檔
