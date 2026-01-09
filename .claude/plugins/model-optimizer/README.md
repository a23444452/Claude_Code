# Model Optimizer Plugin

YOLO 模型優化建議工具，分析模型效能並提供調優建議。

## 功能特色

### 🎯 效能分析
- 模型大小和參數量
- 推論速度測試（CPU/MPS/GPU）
- 記憶體使用分析
- FLOPs 計算

### 📊 訓練分析
- 訓練曲線分析
- 過擬合/欠擬合檢測
- 收斂速度評估
- Early stopping 效果

### 🔧 優化建議
- 模型架構建議（n/s/m/l/x）
- 超參數調整建議
- 資料增強策略
- 訓練技巧推薦

### ⚡ 量化與壓縮
- 模型量化建議（FP16/INT8）
- 剪枝機會分析
- 知識蒸餾建議
- ONNX/TensorRT 匯出

## 使用方式

### 命令
```bash
# 分析最新訓練的模型
/model-optimizer

# 分析指定模型
/model-optimizer --weights runs/train/exp/weights/best.pt

# 包含速度測試
/model-optimizer --benchmark

# 生成完整報告
/model-optimizer --full-report
```

### 輸出範例

```
=== YOLO 模型優化分析 ===

📦 模型資訊:
  架構: YOLO11n
  參數量: 2.59M
  模型大小: 5.5MB
  FLOPs: 6.5G

⚡ 效能測試:
  推論速度 (MPS): 98ms/image
  推論速度 (CPU): 245ms/image
  吞吐量: ~10 images/sec
  記憶體使用: 512MB

📈 訓練分析:
  訓練輪數: 100 epochs
  最佳 mAP@0.5: 0.95 (epoch 87)
  訓練時間: 3.2 分鐘
  收斂狀態: ✓ 已收斂

🎯 效能指標:
  mAP@0.5: 0.95 ⭐ 優秀
  Precision: 0.92 ✓ 良好
  Recall: 0.89 ✓ 良好
  F1-Score: 0.90 ✓ 良好

⚠️ 發現的問題:
  • 訓練曲線在 epoch 60 後趨於平穩，可考慮減少 epochs
  • Recall 略低於 Precision，可能需要降低信心度閾值
  • 無明顯過擬合或欠擬合

💡 優化建議:

1. 速度優化:
   ✓ 當前模型已是最輕量的 YOLO11n
   • 考慮使用 FP16 量化可加速 ~30%
   • 匯出為 ONNX 格式可進一步優化

2. 精度優化:
   • 如需更高精度，建議升級到 YOLO11s (+15% mAP, +2.5M params)
   • 增加訓練資料可能提升 2-3% mAP
   • 調整 conf_threshold 從 0.25 降至 0.2 以提升 Recall

3. 訓練優化:
   • epochs 可降至 80 以節省時間（提前收斂）
   • 可嘗試更激進的資料增強
   • 考慮使用 warmup 和 cosine annealing scheduler

4. 部署優化:
   • 建議匯出 ONNX 格式: yolo export model=best.pt format=onnx
   • 啟用 FP16: yolo export model=best.pt format=onnx half=True
   • TensorRT 可獲得最佳效能（NVIDIA GPU）

🎖️ 綜合評分: 8.5/10
  速度: ⭐⭐⭐⭐⭐ (5/5) - 極快
  精度: ⭐⭐⭐⭐ (4/5) - 優秀
  平衡: ⭐⭐⭐⭐ (4/5) - 良好

結論: 當前模型已經很好地平衡了速度和精度，適合生產環境部署。
```

## 分析項目

### 基礎分析
- ✅ 模型結構和參數量
- ✅ 檔案大小
- ✅ 訓練配置
- ✅ 最佳指標

### 效能分析
- ✅ 推論速度測試
- ✅ 記憶體使用
- ✅ 不同裝置比較
- ✅ 批次處理效能

### 訓練分析
- ✅ 訓練曲線趨勢
- ✅ 過擬合檢測
- ✅ 收斂速度
- ✅ 學習率效果

### 優化機會
- ✅ 架構升級建議
- ✅ 量化可行性
- ✅ 超參數調整
- ✅ 資料策略

## 配置選項

```json
{
  "benchmark": {
    "num_images": 100,
    "warmup_runs": 10,
    "devices": ["cpu", "mps"],
    "image_sizes": [640]
  },
  "thresholds": {
    "good_map": 0.7,
    "excellent_map": 0.9,
    "overfit_gap": 0.1,
    "min_precision": 0.7,
    "min_recall": 0.7
  },
  "recommendations": {
    "enable_quantization_advice": true,
    "enable_architecture_advice": true,
    "enable_training_advice": true,
    "enable_deployment_advice": true
  }
}
```

## 最佳實踐

### 何時使用
1. **訓練完成後**：立即分析模型效能
2. **部署前**：確認模型符合要求
3. **效能問題**：診斷速度或精度問題
4. **選擇模型**：比較不同模型版本

### 優化流程
```bash
# 1. 訓練模型
/train --epochs 100

# 2. 分析效能
/model-optimizer --benchmark

# 3. 根據建議調整
# 4. 重新訓練
# 5. 比較結果
```

### 模型選擇指南

| 模型 | 參數量 | 速度 | 精度 | 適用場景 |
|------|--------|------|------|----------|
| YOLO11n | 2.6M | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 邊緣裝置、即時應用 |
| YOLO11s | 9.4M | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 一般應用、平衡型 |
| YOLO11m | 20.1M | ⭐⭐⭐ | ⭐⭐⭐⭐ | 高精度需求 |
| YOLO11l | 25.3M | ⭐⭐ | ⭐⭐⭐⭐⭐ | 離線處理、精度優先 |
| YOLO11x | 56.9M | ⭐ | ⭐⭐⭐⭐⭐ | 最高精度、伺服器端 |

## 整合建議

與其他工具配合：
```bash
# 完整優化流程
/train                   # 訓練模型
/validate                # 驗證效能
/model-optimizer         # 分析並獲得建議
/quick-predict          # 測試實際效果
```

## 輸出檔案

生成以下報告檔案：
- `analysis/model_report.txt` - 完整分析報告
- `analysis/performance_benchmark.json` - 效能測試數據
- `analysis/optimization_suggestions.md` - 優化建議清單
- `analysis/training_curves.png` - 訓練曲線圖（如果有）

## 進階功能

### 模型比較
```bash
# 比較多個模型
/model-optimizer --compare runs/train/exp*/weights/best.pt
```

### 自動調參建議
基於分析結果自動生成新的訓練配置：
```yaml
# 生成的建議配置
model: yolo11n
epochs: 80  # 從 100 降低
lr0: 0.001  # 調整學習率
augment:
  mosaic: 1.0
  mixup: 0.15  # 增加 mixup
```

### 量化評估
自動測試量化後的效能影響：
- FP32 → FP16: +30% 速度, -0.5% 精度
- FP32 → INT8: +50% 速度, -2% 精度
