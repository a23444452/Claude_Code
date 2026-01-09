# Dataset Analyzer Plugin

YOLO 資料集深度分析工具，提供全面的資料品質檢查和統計分析。

## 功能特色

### 📊 統計分析
- 圖片數量和尺寸分布
- 類別分布和不平衡檢測
- 標註框大小分布
- Train/Val 切分比例

### 🔍 品質檢查
- 遺失的標註檔案
- 空標註檔案（無物件）
- 標註格式錯誤
- 圖片損壞檢測
- 異常大小的圖片

### 📈 視覺化分析
- 類別分布圖表
- 邊界框大小熱圖
- 圖片尺寸分布
- 物件密度分析

### ⚠️ 問題偵測
- 類別不平衡警告（差異 > 3倍）
- 過小或過大的標註框
- 標註邊界異常（超出圖片範圍）
- 重複圖片檢測

## 使用方式

### 命令
```bash
# 分析預處理後的資料集
/dataset-analyzer

# 分析指定資料集
/dataset-analyzer --path dataset/my_dataset

# 輸出詳細報告
/dataset-analyzer --verbose

# 生成視覺化圖表
/dataset-analyzer --visualize
```

### 輸出範例

```
=== YOLO 資料集分析報告 ===

📁 資料集: dataset/MBB_gray_processed/

📊 基本統計:
  總圖片數: 37 張
  訓練集: 29 張 (78.4%)
  驗證集: 8 張 (21.6%)
  總標註數: 156 個物件

📐 圖片尺寸:
  平均尺寸: 1280x720
  最小尺寸: 640x480
  最大尺寸: 1920x1080

🏷️ 類別分布:
  類別 0: 45 個 (28.8%)
  類別 1: 38 個 (24.4%)
  類別 2: 29 個 (18.6%)
  ...

⚠️ 發現的問題:
  ✗ 類別 0 和類別 9 數量差異過大 (4.5倍)
  ✗ 發現 3 個異常小的標註框 (< 10x10 pixels)
  ✓ 無遺失的標註檔案
  ✓ 無損壞的圖片

💡 建議:
  • 考慮對類別 9 進行資料增強
  • 檢查異常小標註框是否為標註錯誤
  • 資料集整體品質良好
```

## 檢查項目

### 必要檢查
- ✅ 圖片與標註檔案配對
- ✅ 標註格式正確性
- ✅ 類別 ID 在有效範圍內
- ✅ 座標值在 [0, 1] 範圍內

### 品質檢查
- ✅ 類別分布平衡性
- ✅ 標註框大小合理性
- ✅ 圖片尺寸一致性
- ✅ 物件密度適當性

### 進階檢查
- ✅ 重複或相似圖片
- ✅ 異常的長寬比
- ✅ 標註密集度分析
- ✅ 資料增強建議

## 配置選項

在 `.claude-plugin/config.json` 中可配置：

```json
{
  "thresholds": {
    "class_imbalance_ratio": 3.0,
    "min_bbox_size": 10,
    "max_bbox_size": 800,
    "min_image_size": 320,
    "max_image_size": 4096
  },
  "checks": {
    "enable_duplicate_detection": true,
    "enable_visualization": true,
    "enable_advanced_stats": true
  }
}
```

## 輸出檔案

分析完成後會在 `analysis/` 目錄生成：
- `dataset_report.txt` - 文字報告
- `class_distribution.png` - 類別分布圖
- `bbox_size_heatmap.png` - 標註框大小熱圖
- `image_size_distribution.png` - 圖片尺寸分布圖

## 最佳實踐

1. **訓練前必做**：在開始訓練前先運行分析，確保資料品質
2. **定期檢查**：新增資料後重新分析
3. **問題修復**：根據建議修正資料集問題
4. **記錄追蹤**：保存分析報告以追蹤資料集變化

## 整合建議

與其他 commands 搭配使用：
```bash
# 完整工作流程
/preprocess              # 預處理資料集
/dataset-analyzer        # 分析資料品質
/train                   # 開始訓練
```

## 技術細節

- 使用 Python PIL/OpenCV 進行圖片分析
- 使用 NumPy 進行統計計算
- 支援 YOLO 標註格式（class_id x_center y_center width height）
- 多執行緒加速大資料集分析
