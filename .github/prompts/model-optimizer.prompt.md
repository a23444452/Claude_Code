# 模型優化助手提示模板

## 用途
協助分析模型效能、提供優化建議，改善推論速度、記憶體使用和準確度。

## 使用方式
將此提示模板貼到 Claude Code 中，並替換 `[...]` 中的內容為你的實際資訊。

---

## 提示模板

```
我需要優化我的 YOLO 模型效能，請協助分析和改進。

### 模型資訊
- 模型: [例如: yolo11n, yolo11s, 自訓練模型]
- 模型路徑: [例如: runs/detect/train/weights/best.pt]
- 模型大小: [MB]
- 類別數量: [數量]

### 效能指標
#### 準確度
- mAP@0.5: [數值]
- mAP@0.5:0.95: [數值]
- Precision: [數值]
- Recall: [數值]

#### 速度
- 推論時間: [ms] per image
- FPS: [數值]
- 裝置: [CPU/MPS/CUDA]

#### 資源使用
- 記憶體使用: [GB]
- 模型大小: [MB]

### 優化目標
[選擇你的主要目標]
- [ ] 提升準確度
- [ ] 提升推論速度
- [ ] 減少記憶體使用
- [ ] 減小模型大小（部署需求）
- [ ] 平衡準確度和速度

### 應用場景
[描述實際應用場景]
- 部署環境: [邊緣裝置/伺服器/雲端]
- 即時性需求: [是/否，需要達到多少 FPS]
- 硬體限制: [記憶體、運算能力限制]

### 當前問題（如有）
[描述遇到的具體問題]
- 推論太慢
- 記憶體不足
- 準確度不夠
- 模型太大無法部署

請協助我：
1. 使用 `/model-optimizer --model [模型路徑] --analyze` 分析模型
2. 解讀優化報告
3. 根據我的目標提供具體優化建議
4. 提供實作步驟和程式碼範例
```

---

## 使用流程

### Step 1: 執行模型分析
```bash
/model-optimizer --model runs/detect/train/weights/best.pt --analyze
```

### Step 2: 提供分析結果
將優化報告內容貼到對話中，讓 Claude 解讀並提供建議。

### Step 3: 實施優化
根據建議進行優化，可能包括：
- 模型量化（Quantization）
- 模型剪枝（Pruning）
- 知識蒸餾（Knowledge Distillation）
- 超參數調整
- 改用更合適的模型大小

### Step 4: 驗證效果
優化後重新測試效能，確認改進效果。

---

## 範例使用

### 範例 1: 邊緣裝置部署優化
```
我需要優化我的 YOLO 模型效能，請協助分析和改進。

### 模型資訊
- 模型: yolo11s (自訓練)
- 模型路徑: runs/detect/train/weights/best.pt
- 模型大小: 22MB
- 類別數量: 3

### 效能指標
#### 準確度
- mAP@0.5: 0.85
- mAP@0.5:0.95: 0.68
- Precision: 0.82
- Recall: 0.78

#### 速度
- 推論時間: 150ms per image
- FPS: ~6.5
- 裝置: Raspberry Pi 4 (CPU)

### 優化目標
- [x] 提升推論速度
- [x] 減小模型大小
- [ ] 準確度可以略為犧牲（接受度 ±5%）

### 應用場景
需要部署到 Raspberry Pi 進行即時監控，希望達到至少 15 FPS。
記憶體限制 2GB，需要模型小於 10MB。

請提供優化建議和實作步驟。
```

### 範例 2: 準確度提升優化
```
我需要優化我的 YOLO 模型效能，請協助分析和改進。

### 模型資訊
- 模型: yolo11n (自訓練)
- 類別數量: 5（工業瑕疵檢測）

### 效能指標
#### 準確度
- mAP@0.5: 0.62
- mAP@0.5:0.95: 0.41
- Precision: 0.65
- Recall: 0.58

#### 速度
- 推論時間: 25ms per image
- 裝置: NVIDIA RTX 3080

### 優化目標
- [x] 提升準確度（目標 mAP@0.5 > 0.80）
- [ ] 速度不是主要考量（可接受較慢）

### 當前問題
準確度不夠高，尤其是小瑕疵的偵測效果差。

### Model Optimizer 報告
```
[貼上 /model-optimizer 的完整輸出]
```

請提供提升準確度的優化建議。
```

### 範例 3: 平衡優化
```
我需要優化我的 YOLO 模型效能，請協助分析和改進。

### 模型資訊
- 模型: yolo11m (自訓練)
- 模型大小: 52MB

### 效能指標
- mAP@0.5: 0.88
- 推論時間: 80ms per image (GPU)
- 記憶體使用: 4GB

### 優化目標
- [x] 平衡準確度和速度
- [x] 減少記憶體使用（目標 < 2GB）

### 應用場景
雲端 API 服務，需要處理並發請求。
目前記憶體使用太高，無法同時處理多個請求。

請協助分析並提供優化方案。
```

---

## 常見優化策略

### 1. 模型大小選擇
```
yolo11n (2.6M params) → 最快，準確度較低
yolo11s (9.4M params) → 快速，準確度中等
yolo11m (20.1M params) → 平衡
yolo11l (25.3M params) → 慢，準確度高
yolo11x (56.9M params) → 最準確，最慢
```

**選擇建議**:
- 邊緣裝置: n 或 s
- 伺服器/雲端: m 或 l
- 高準確度需求: l 或 x

### 2. 推論優化技術

#### 模型量化 (Quantization)
```python
# INT8 量化（準確度略降，速度提升 2-4x）
from ultralytics import YOLO

model = YOLO("best.pt")
model.export(format="onnx", int8=True)
```

#### 批次推論
```python
# 處理多張圖片時使用批次推論
results = model.predict(images, batch=16)  # 提升吞吐量
```

#### 圖片大小調整
```python
# 降低輸入解析度（速度提升，準確度可能略降）
results = model.predict(image, imgsz=416)  # 預設 640
```

### 3. 硬體加速

#### GPU 加速
```python
# 使用 GPU 推論
model = YOLO("best.pt")
results = model.predict(image, device=0)  # CUDA device 0
```

#### Apple Silicon (MPS)
```python
# M1/M2 Mac 使用 MPS 加速
results = model.predict(image, device="mps")
```

#### TensorRT 優化
```python
# NVIDIA GPU 使用 TensorRT（速度提升 2-5x）
model.export(format="engine")  # 匯出 TensorRT engine
```

### 4. 訓練優化

#### 更好的資料增強
```python
# 增加資料多樣性
model.train(
    data="data.yaml",
    augment=True,
    hsv_h=0.015,  # 色調變化
    hsv_s=0.7,    # 飽和度
    hsv_v=0.4,    # 明度
    degrees=10,   # 旋轉
    translate=0.1, # 平移
    scale=0.5,    # 縮放
    flipud=0.5,   # 垂直翻轉
)
```

#### 使用預訓練模型
```python
# 遷移學習（Transfer Learning）
model = YOLO("yolo11n.pt")  # 使用預訓練權重
model.train(data="data.yaml", epochs=100)
```

---

## 效能基準參考

### YOLO11 系列效能比較（COCO dataset）

| 模型 | 參數量 | mAP@0.5:0.95 | 速度 (ms) | 模型大小 |
|------|--------|--------------|-----------|----------|
| n | 2.6M | 39.5 | 1.5 | 6MB |
| s | 9.4M | 47.0 | 2.3 | 22MB |
| m | 20.1M | 51.5 | 4.5 | 50MB |
| l | 25.3M | 53.4 | 6.5 | 58MB |
| x | 56.9M | 54.7 | 10.6 | 138MB |

*速度基於 NVIDIA V100 GPU

---

## 優化檢查清單

### 準確度優化
- [ ] 使用更大的模型（s → m → l）
- [ ] 增加訓練 epochs
- [ ] 改善資料集品質和數量
- [ ] 調整資料增強參數
- [ ] 使用更大的 `imgsz`
- [ ] 調整 confidence 和 IoU 閾值

### 速度優化
- [ ] 使用更小的模型（m → s → n）
- [ ] 降低 `imgsz`
- [ ] 使用模型量化（INT8/FP16）
- [ ] 使用 TensorRT/ONNX Runtime
- [ ] 啟用 GPU/MPS 加速
- [ ] 批次推論處理多圖片

### 記憶體優化
- [ ] 使用更小的模型
- [ ] 降低批次大小
- [ ] 使用模型量化
- [ ] 減少 `imgsz`
- [ ] 使用模型剪枝技術

### 部署優化
- [ ] 匯出為優化格式（ONNX/TensorRT）
- [ ] 移除不必要的輸出
- [ ] 使用模型壓縮技術
- [ ] 考慮知識蒸餾

---

## 提示技巧

1. **使用分析工具**: 先執行 `/model-optimizer` 獲得基準數據
2. **明確目標**: 清楚說明優化目標（速度/準確度/大小）
3. **提供場景**: 描述實際部署環境和限制
4. **測試驗證**: 每次優化後測試並記錄效果
5. **漸進式優化**: 一次嘗試一種優化方法，觀察效果
6. **效能監控**: 持續監控推論時間、記憶體使用
