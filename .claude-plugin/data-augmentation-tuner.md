# Data Augmentation Tuner Plugin

## Description
資料增強策略優化器，根據資料集特性推薦最佳的增強參數組合。

## Augmentation Parameters

### Color Space
- `hsv_h`: 色調抖動 (0.015)
- `hsv_s`: 飽和度 (0.7)
- `hsv_v`: 明度 (0.4)

### Geometric
- `degrees`: 旋轉 (0-45°)
- `translate`: 平移 (0.1)
- `scale`: 縮放 (0.5)
- `shear`: 剪切 (0.0)

### Mosaic & MixUp
- `mosaic`: Mosaic 增強 (1.0)
- `mixup`: MixUp 增強 (0.0-0.1)

## Recommendations by Dataset Size

| 資料集大小 | 增強強度 | 建議 |
|-----------|---------|------|
| < 300 | 高 | 啟用所有增強 |
| 300-1000 | 中 | 標準增強 |
| > 1000 | 低 | 基本增強 |

## Version History
- v1.0.0: 初始版本
