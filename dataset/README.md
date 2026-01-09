# Dataset 目錄說明

此目錄用於存放 YOLO 訓練所需的資料集。

⚠️ **注意：此目錄已加入 .gitignore，不會被 commit 到 Git。**

## 資料集結構

標準的 YOLO 資料集結構如下：

```
dataset/
└── your_dataset_name/
    ├── images/
    │   ├── train/          # 訓練集圖片
    │   │   ├── image1.jpg
    │   │   ├── image2.jpg
    │   │   └── ...
    │   └── val/            # 驗證集圖片
    │       ├── image1.jpg
    │       ├── image2.jpg
    │       └── ...
    ├── labels/
    │   ├── train/          # 訓練集標註
    │   │   ├── image1.txt
    │   │   ├── image2.txt
    │   │   └── ...
    │   └── val/            # 驗證集標註
    │       ├── image1.txt
    │       ├── image2.txt
    │       └── ...
    └── classes.txt         # 類別清單（選用）
```

## YOLO 標註格式

每個圖片對應一個同名的 `.txt` 標註檔案。

### 標註檔案格式
每行代表一個物件：
```
class_id x_center y_center width height
```

**參數說明：**
- `class_id`: 類別 ID，從 0 開始（整數）
- `x_center`: 邊界框中心 X 座標（0-1 之間的浮點數）
- `y_center`: 邊界框中心 Y 座標（0-1 之間的浮點數）
- `width`: 邊界框寬度（0-1 之間的浮點數）
- `height`: 邊界框高度（0-1 之間的浮點數）

**範例：**
```
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.15 0.2
0 0.8 0.7 0.25 0.3
```

### 座標計算方式

假設圖片尺寸為 1280x720，物件邊界框為 (100, 200, 300, 400)：

```python
# 原始座標（像素）
x_min, y_min = 100, 200
x_max, y_max = 300, 400
image_width, image_height = 1280, 720

# 轉換為 YOLO 格式
x_center = ((x_min + x_max) / 2) / image_width  = 0.156
y_center = ((y_min + y_max) / 2) / image_height = 0.417
width = (x_max - x_min) / image_width           = 0.156
height = (y_max - y_min) / image_height         = 0.278

# 標註檔案內容
0 0.156 0.417 0.156 0.278
```

## 準備資料集

### 方法 1: 使用現有資料集
如果你已有標註好的資料集：

1. 將資料集放入此目錄
2. 確認結構符合上述格式
3. 更新 `config/data.yaml` 的路徑

### 方法 2: 手動標註
使用標註工具標註圖片：

**推薦標註工具：**
- [LabelImg](https://github.com/heartexlabs/labelImg) - 經典標註工具
- [CVAT](https://github.com/opencv/cvat) - 強大的線上標註平台
- [Roboflow](https://roboflow.com/) - 雲端標註和資料管理
- [Label Studio](https://labelstud.io/) - 開源標註平台

**標註步驟：**
1. 使用工具載入圖片
2. 框選物件並標記類別
3. 匯出為 YOLO 格式
4. 放入對應的 images/ 和 labels/ 目錄

### 方法 3: 從其他格式轉換
如果你的標註是其他格式（如 COCO、Pascal VOC）：

```bash
# 使用資料預處理工具轉換
python src/utils/preprocess.py --convert --format coco
```

## 資料集檢查

使用 Dataset Analyzer plugin 檢查資料集品質：

```bash
/dataset-analyzer
```

這會檢查：
- ✅ 圖片與標註檔案配對
- ✅ 標註格式正確性
- ✅ 類別分布
- ✅ 標註框大小
- ✅ 資料品質問題

## 資料集切分

### 自動切分
使用預處理工具自動切分 train/val：

```bash
python src/utils/preprocess.py \
  --source dataset/raw_data \
  --output dataset/processed_data \
  --train-ratio 0.8
```

### 手動切分
建議比例：
- **訓練集 (train)**: 70-80%
- **驗證集 (val)**: 20-30%
- **測試集 (test)**: 選用，通常 10-20%

## 資料增強

YOLO 訓練時會自動進行資料增強，包括：
- 隨機縮放和裁剪
- 隨機翻轉
- 顏色抖動
- Mosaic 增強
- MixUp 增強

可在 `config/data.yaml` 中調整增強參數。

## 資料集大小建議

| 任務類型 | 建議圖片數量 | 說明 |
|---------|-------------|------|
| 簡單場景 | 500-1000 | 背景單純、物件清晰 |
| 一般場景 | 1000-5000 | 一般複雜度 |
| 複雜場景 | 5000+ | 多類別、複雜背景 |
| 工業應用 | 100-500 per class | 高品質標註更重要 |

## 常見問題

### Q1: 如何檢查標註是否正確？
A: 使用視覺化工具或寫簡單腳本繪製邊界框：
```python
from PIL import Image, ImageDraw

# 讀取圖片和標註
img = Image.open('image.jpg')
with open('image.txt') as f:
    for line in f:
        cls, x, y, w, h = map(float, line.split())
        # 轉換為像素座標
        x1 = (x - w/2) * img.width
        y1 = (y - h/2) * img.height
        x2 = (x + w/2) * img.width
        y2 = (y + h/2) * img.height
        # 繪製邊界框
        draw = ImageDraw.Draw(img)
        draw.rectangle([x1, y1, x2, y2], outline='red', width=2)
img.show()
```

### Q2: 標註檔案是否需要包含沒有物件的圖片？
A: 可以包含，空標註檔案（0 行）代表該圖片沒有物件。這對訓練減少誤報很有幫助。

### Q3: 圖片格式有限制嗎？
A: YOLO 支援常見格式：`.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`。建議使用 `.jpg` 或 `.png`。

### Q4: 圖片尺寸需要統一嗎？
A: 不需要。YOLO 訓練時會自動 resize 到指定大小（通常 640x640）。但建議長寬比不要相差太大。

### Q5: 如何處理小物件？
A:
- 使用更高的輸入解析度（如 1280）
- 增加小物件的訓練樣本
- 調整 anchor boxes
- 使用專門的小物件檢測模型

## 資料集管理

### 版本控制
資料集不適合 Git 管理，建議使用：
- **[DVC (Data Version Control)](https://dvc.org/)** - 專門的資料版本控制
- **雲端儲存** - Google Drive, S3, Azure Blob
- **內部伺服器** - NAS, 檔案伺服器

### 資料集分享
團隊協作時，建議：
1. 將資料集上傳到雲端
2. 在 README 中提供下載連結
3. 提供 MD5 checksum 確保完整性
4. 記錄資料集版本和更新日誌

## 相關資源

- [YOLO 官方文檔](https://docs.ultralytics.com/)
- [Roboflow Universe](https://universe.roboflow.com/) - 公開資料集
- [Open Images Dataset](https://storage.googleapis.com/openimages/web/index.html)
- [COCO Dataset](https://cocodataset.org/)

## 檢查清單

準備好資料集後，確認以下項目：
- [ ] 資料集結構正確（images/ 和 labels/ 目錄）
- [ ] 每個圖片都有對應的標註檔案
- [ ] 標註格式符合 YOLO 規範
- [ ] 已切分 train/val 集
- [ ] 已更新 config/data.yaml
- [ ] 執行 `/dataset-analyzer` 檢查品質
- [ ] 無明顯的標註錯誤或遺漏
