# YOLO 物件偵測系統 - 完整使用指南

## 系統概覽

完整的 YOLO 物件偵測系統，包含：
- ✅ 資料預處理
- ✅ 模型訓練
- ✅ FastAPI 後端
- ✅ Web 前端介面

---

## 快速開始

### 1. 啟動後端 API

```bash
cd /Users/vincewang/YOLO_Project
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

後端將運行在: **http://localhost:8000**
- API 文檔: http://localhost:8000/docs
- 健康檢查: http://localhost:8000/health

### 2. 啟動前端介面

開啟新的終端視窗：

```bash
cd /Users/vincewang/YOLO_Project/src/frontend
./start_frontend.sh
```

前端將運行在: **http://localhost:3000**

### 3. 開始使用

1. 在瀏覽器中開啟 http://localhost:3000
2. 上傳圖片（點擊或拖曳）
3. 調整參數（選用）
4. 點擊「開始偵測」
5. 查看結果！

---

## 完整工作流程

### 階段 1: 資料準備

#### 1.1 準備原始資料
將圖片和對應的 YOLO 格式標註放入資料夾：
```
dataset/
└── MBB_gray_dataset/
    ├── image1.jpg
    ├── image1.txt
    ├── image2.jpg
    ├── image2.txt
    └── ...
```

#### 1.2 執行資料預處理
```bash
~/miniforge3/envs/YOLO_env/bin/python src/utils/preprocess.py \
  --source dataset/MBB_gray_dataset \
  --output dataset/MBB_gray_processed \
  --train-ratio 0.8
```

這會：
- ✓ 驗證圖片完整性
- ✓ 轉換為 RGB 格式
- ✓ 驗證標註格式
- ✓ 隨機切分 train/val
- ✓ 生成 classes.txt

#### 1.3 創建配置檔
```bash
# 已自動創建在 config/data_gray.yaml
```

---

### 階段 2: 模型訓練

#### 2.1 測試環境
```bash
~/miniforge3/envs/YOLO_env/bin/python src/training/train.py --mode test
```

#### 2.2 開始訓練
```bash
~/miniforge3/envs/YOLO_env/bin/python src/training/train.py \
  --mode train \
  --data config/data_gray.yaml \
  --batch 8 \
  --augment \
  --epochs 100
```

訓練參數說明：
- `--mode train`: 訓練模式
- `--data`: 資料配置檔
- `--model`: 模型大小 (n/s/m/l/x)，預設 n
- `--batch`: 批次大小，建議 4-16
- `--augment`: 啟用資料增強
- `--epochs`: 訓練輪數
- `--imgsz`: 圖片大小，預設 640

#### 2.3 監控訓練
訓練結果儲存在：
```
runs/train/exp/
├── weights/
│   ├── best.pt      # 最佳模型
│   └── last.pt      # 最後模型
├── results.png      # 訓練曲線
└── ...
```

#### 2.4 驗證模型
```bash
~/miniforge3/envs/YOLO_env/bin/python src/training/train.py \
  --mode validate \
  --weights runs/train/exp/weights/best.pt \
  --data config/data_gray.yaml
```

---

### 階段 3: 部署後端 API

#### 3.1 啟動服務
```bash
# 開發模式
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 生產模式（多 worker）
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 3.2 測試 API
```bash
# 使用測試腳本
~/miniforge3/envs/YOLO_env/bin/python src/api/test_api.py

# 或使用 curl
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test.jpg" \
  -F "conf_threshold=0.3"
```

#### 3.3 查看 API 文檔
訪問 http://localhost:8000/docs 查看完整 API 文檔

---

### 階段 4: 使用前端介面

#### 4.1 啟動前端
```bash
cd src/frontend
./start_frontend.sh
```

#### 4.2 使用介面
1. 開啟 http://localhost:3000
2. 上傳圖片
3. 調整參數
4. 查看偵測結果

---

## API 使用範例

### Python
```python
import requests

# 偵測單張圖片
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
for det in result['detections']:
    print(f"- {det['class_name']}: {det['confidence']:.2%}")
```

### JavaScript
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict?conf_threshold=0.3', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log(`偵測到 ${data.detection_count} 個物件`);
    data.detections.forEach(det => {
        console.log(`${det.class_name}: ${(det.confidence * 100).toFixed(1)}%`);
    });
});
```

### cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test.jpg" \
  -F "conf_threshold=0.3" | jq .
```

---

## 專案結構

```
YOLO_Project/
├── config/
│   ├── data.yaml          # 原始資料集配置
│   └── data_gray.yaml     # 灰階資料集配置
├── dataset/
│   ├── MBB_Dataset/       # 原始資料集
│   ├── MBB_gray_dataset/  # 灰階原始資料
│   └── MBB_gray_processed/ # 預處理後資料
├── models/                # 模型檔案（建議 .gitignore）
├── runs/                  # 訓練結果
│   └── train/
│       └── exp/
│           └── weights/
│               ├── best.pt
│               └── last.pt
├── src/
│   ├── api/
│   │   ├── main.py        # FastAPI 主程式
│   │   ├── test_api.py    # API 測試
│   │   └── README.md
│   ├── frontend/
│   │   ├── index.html     # 前端頁面
│   │   ├── app.js         # 前端邏輯
│   │   └── README.md
│   ├── training/
│   │   └── train.py       # 訓練腳本
│   └── utils/
│       └── preprocess.py  # 資料預處理
├── CLAUDE.md              # 專案規範
└── USAGE.md               # 本文件
```

---

## 常見問題

### Q1: 訓練時記憶體不足
**A**: 降低 batch size
```bash
--batch 4  # 或更小
```

### Q2: API 無法連接
**A**: 確認服務已啟動
```bash
curl http://localhost:8000/health
```

### Q3: 前端顯示 CORS 錯誤
**A**: 後端已配置 CORS，確認 API 端點正確

### Q4: 偵測結果不理想
**A**: 調整參數：
- 降低 `conf_threshold` (例如 0.2)
- 增加訓練資料
- 使用更大的模型 (s/m/l)

### Q5: 訓練速度慢
**A**:
- 確認使用 MPS 加速（Mac M1/M2/M3）
- 降低 `imgsz`（例如 416）
- 使用更小的模型 (nano)

---

## 效能優化

### 訓練優化
```bash
# 使用小圖片加快訓練
--imgsz 416

# 增加 batch size（如果記憶體足夠）
--batch 16

# 減少 patience 提早停止
--patience 20
```

### API 優化
```python
# 使用多 worker
uvicorn src.api.main:app --workers 4

# 啟用快取
# 在 main.py 中實作快取機制
```

### 前端優化
```javascript
// 壓縮圖片再上傳
compressImage(file, maxSize=1920)

// 使用 WebWorker 處理大圖
const worker = new Worker('image-worker.js')
```

---

## 部署指南

### Docker 部署

#### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./runs:/app/runs

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./src/frontend:/usr/share/nginx/html
```

### 雲端部署

#### Heroku
```bash
heroku create yolo-detection-api
git push heroku main
```

#### AWS / GCP / Azure
參考各平台文檔部署 FastAPI 應用

---

## 監控與日誌

### 查看 API 日誌
```bash
tail -f /var/log/uvicorn.log
```

### 監控指標
- 請求數量
- 平均回應時間
- 錯誤率
- GPU/CPU 使用率

---

## 授權與貢獻

本專案遵循 [專案授權]

歡迎提交 Issue 和 Pull Request！

---

## 聯絡方式

如有問題，請聯絡：[你的聯絡資訊]
