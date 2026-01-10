# YOLO Training Advisor Plugin

## Description
專業的 YOLO 訓練顧問，協助優化超參數、偵測過擬合/欠擬合問題，並提供訓練策略建議。

## Capabilities
- 🎯 超參數優化建議（learning rate, batch size, epochs）
- 📊 訓練曲線分析（loss, mAP, precision, recall）
- 🔍 過擬合/欠擬合診斷
- 💡 資料增強策略建議
- 🚀 訓練加速技巧
- 📈 效能瓶頸分析

## When to Use
- 開始新的訓練任務
- 訓練效果不理想
- Loss 不下降或震盪
- 驗證集表現遠差於訓練集
- 需要優化訓練速度

## Usage

### Example 1: 診斷過擬合問題
```
User: 我的模型訓練集 mAP 達到 0.92，但驗證集只有 0.65，該如何改善？

Plugin Response:
這是典型的過擬合問題。建議採取以下措施：

1. **增加正則化**：
   - 啟用 dropout (如果可用)
   - 增加 weight decay

2. **資料增強**：
   - 增加 hsv 色彩抖動: hsv_h=0.015, hsv_s=0.7, hsv_v=0.4
   - 啟用 mosaic 增強: mosaic=1.0
   - 增加 mixup: mixup=0.1
   - 增加幾何變換: degrees=10, scale=0.5

3. **Early Stopping**：
   - 設定 patience=50，避免過度訓練
   - 監控驗證集 mAP，保存最佳模型

4. **收集更多資料**：
   - 如果可能，增加訓練資料多樣性
   - 確保訓練/驗證集分布一致

實作範例：
```python
model.train(
    data='data.yaml',
    epochs=100,
    patience=50,  # Early stopping
    # 資料增強
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=10,
    scale=0.5,
    mosaic=1.0,
    mixup=0.1,
)
```
```

### Example 2: 訓練速度優化
```
User: 訓練速度很慢，有什麼加速方法？

Plugin Response:
提供以下加速策略：

1. **批次大小優化**：
   - 增加 batch size（在記憶體允許範圍內）
   - 使用 batch=16 或 32（取決於 GPU 記憶體）

2. **圖片大小調整**：
   - 降低 imgsz（如 640 → 512）
   - 僅在必要時使用大尺寸

3. **模型選擇**：
   - 使用較小的模型（yolo11n 或 yolo11s）進行快速實驗
   - 確定超參數後再用大模型

4. **硬體加速**：
   - 使用 GPU: device=0（CUDA）或 device='mps'（Apple Silicon）
   - 啟用混合精度訓練（自動啟用）

5. **減少資料增強計算**：
   - 暫時降低 mosaic/mixup 強度進行測試

6. **Workers 優化**：
   - 增加 workers 數量: workers=8

實作範例：
```python
model.train(
    data='data.yaml',
    epochs=100,
    batch=32,      # 增加批次
    imgsz=512,     # 降低解析度
    device=0,      # 使用 GPU
    workers=8,     # 多執行緒載入
)
```
```

### Example 3: Loss 不下降診斷
```
User: Loss 一直維持在 2.5 左右不下降，該怎麼辦？

Plugin Response:
Loss 停滯可能有多種原因：

1. **學習率問題**：
   - 可能學習率太低：嘗試 lr0=0.01（預設）或更高
   - 可能已過優化：嘗試降低學習率 lr0=0.001

2. **資料集問題**：
   - 檢查標註是否正確（使用 /dataset-analyzer）
   - 確認類別分布是否平衡
   - 驗證圖片品質

3. **模型容量**：
   - 若使用 yolo11n，嘗試 yolo11s 或 yolo11m
   - 較大模型有更強的學習能力

4. **訓練策略**：
   - 增加訓練 epochs（100 → 200）
   - 使用預訓練權重（COCO）
   - 啟用遷移學習

診斷步驟：
```bash
# 1. 驗證資料集
python scripts/validate_dataset.py config/data.yaml -v

# 2. 檢查訓練日誌
tail -f runs/detect/train/results.csv

# 3. 視覺化訓練曲線
# 查看 runs/detect/train/results.png
```

調整建議：
```python
# 嘗試較大模型
model = YOLO('yolo11s.pt')  # 改用 small

# 調整學習率
model.train(
    data='data.yaml',
    epochs=200,
    lr0=0.01,      # 初始學習率
    lrf=0.001,     # 最終學習率
)
```
```

## Best Practices

### 訓練前檢查清單
- [ ] 資料集已驗證（使用 `/dataset-analyzer`）
- [ ] 類別分布合理（無嚴重不平衡）
- [ ] 標註格式正確（YOLO format）
- [ ] 配置檔案正確（data.yaml）
- [ ] 已選擇合適的模型大小

### 監控指標
- **主要指標**: mAP@0.5, mAP@0.5:0.95
- **輔助指標**: Precision, Recall, Loss
- **過擬合指標**: train_loss vs val_loss 差距

### 常見問題解決

#### 過擬合 (Overfitting)
- 症狀: 訓練集表現好，驗證集差
- 解決: 資料增強、早停、收集更多資料

#### 欠擬合 (Underfitting)
- 症狀: 訓練集和驗證集都表現差
- 解決: 增加模型容量、訓練更多 epochs、檢查資料品質

#### 類別不平衡
- 症狀: 某些類別 Recall 很低
- 解決: 過採樣、加權損失、收集更多少數類別資料

## Integration with Other Tools

### 配合使用的工具
- `/dataset-analyzer` - 訓練前驗證資料集
- `/model-optimizer` - 訓練後優化模型
- `/training-monitor` - 即時監控訓練過程

### 工作流程建議
```
1. 驗證資料集 (dataset-quality-guard)
   ↓
2. 開始訓練 (yolo-training-advisor)
   ↓
3. 監控進度 (training-monitor)
   ↓
4. 優化模型 (model-deployment-assistant)
```

## Technical Details

### 支援的 YOLO 版本
- YOLOv11 (推薦)
- YOLOv8
- YOLOv5 (有限支援)

### 訓練參數說明

#### 基礎參數
- `epochs`: 訓練輪數（100-300）
- `batch`: 批次大小（8-32，取決於記憶體）
- `imgsz`: 圖片大小（640, 1280）
- `device`: 裝置（cpu, mps, 0, 1）

#### 優化參數
- `lr0`: 初始學習率（0.01）
- `lrf`: 最終學習率（0.001）
- `momentum`: 動量（0.937）
- `weight_decay`: 權重衰減（0.0005）

#### 資料增強參數
- `hsv_h`, `hsv_s`, `hsv_v`: 色彩空間抖動
- `degrees`: 旋轉角度
- `translate`: 平移
- `scale`: 縮放
- `mosaic`: Mosaic 增強
- `mixup`: MixUp 增強

## Examples

### 完整訓練範例
```python
from ultralytics import YOLO

# 載入模型
model = YOLO('yolo11s.pt')

# 訓練
results = model.train(
    # 基礎配置
    data='config/data.yaml',
    epochs=100,
    batch=16,
    imgsz=640,
    device='mps',  # or 'cuda:0' or 'cpu'

    # 優化參數
    lr0=0.01,
    lrf=0.001,
    patience=50,  # Early stopping

    # 資料增強
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=10,
    translate=0.1,
    scale=0.5,
    mosaic=1.0,
    mixup=0.0,

    # 其他
    save=True,
    save_period=10,  # 每 10 epochs 儲存
    plots=True,
)
```

## Troubleshooting

### Q: 如何判斷是否過擬合？
A: 觀察 `runs/detect/train/results.png` 中的 train/val loss 曲線。如果 train loss 持續下降但 val loss 開始上升，即為過擬合。

### Q: 訓練多少 epochs 合適？
A: 通常 100-300 epochs。使用 `patience=50` 讓模型自動早停。

### Q: 如何選擇模型大小？
A:
- 快速實驗/邊緣裝置: yolo11n
- 一般用途: yolo11s 或 yolo11m
- 高準確度: yolo11l 或 yolo11x

## Version History
- v1.0.0: 初始版本，支援 YOLOv11 訓練優化
