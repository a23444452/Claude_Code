---
name: data-pipeline
description: 處理影像收集、資料增強 (Augmentation) 與標註格式轉換。
---

# Data Pipeline

## Label Format
專案使用標準 YOLO 格式：
`class_id center_x center_y width height` (全部正規化為 0-1 之間)

## Pre-processing
在訓練前，請使用 `src/utils/preprocess.py` 檢查：
1. 圖片是否損毀
2. Label 座標是否超出邊界
3. 轉換非 RGB 圖片
