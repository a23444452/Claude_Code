# 專案狀態總覽

顯示 YOLO 專案的完整狀態總覽。

## 執行步驟

檢查並顯示以下資訊：

### 1. 資料集狀態
- 原始資料集數量
- 預處理資料集數量
- Train/Val 切分比例
- 類別數量

### 2. 模型狀態
- 訓練次數（runs/train/ 下的 exp 數量）
- 最新模型路徑和大小
- 最佳模型效能指標（如果有）

### 3. 服務狀態
- API 服務運行狀態（port 8000）
- 前端服務運行狀態（port 3000）
- 服務可訪問性

### 4. Git 狀態
- 當前分支
- 未提交的變更
- 與遠端的同步狀態

### 5. 環境資訊
- Python 版本
- PyTorch 版本
- Ultralytics 版本
- 可用的加速裝置（MPS/CUDA/CPU）

## 使用範例

```bash
# 查看完整專案狀態
/project-status
```

## 輸出範例

```
=== YOLO 專案狀態 ===

資料集：
  原始: 38 張圖片
  訓練集: 29 張 (80%)
  驗證集: 8 張 (20%)
  類別數: 10

模型：
  最新: runs/train/exp/weights/best.pt (5.5MB)
  訓練輪數: 100 epochs
  mAP@0.5: 0.95

服務：
  ✓ API 運行中 (http://localhost:8000)
  ✓ 前端運行中 (http://localhost:3000)

Git：
  分支: main
  狀態: 已同步 origin/main
  未提交變更: 0

環境：
  Python: 3.10.13
  PyTorch: 2.9.1
  加速: MPS (Apple Silicon)
```
