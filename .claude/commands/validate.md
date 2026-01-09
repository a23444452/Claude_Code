# 驗證模型效能

在驗證集上驗證 YOLO 模型的效能表現。

## 執行步驟

1. 檢查模型權重檔案是否存在
2. 檢查驗證集是否存在
3. 執行驗證：
   - 載入最佳模型（best.pt）
   - 在驗證集上進行推論
   - 計算 mAP、Precision、Recall 等指標
4. 顯示驗證結果和混淆矩陣

## 使用範例

```bash
# 驗證最新模型
/validate

# 驗證指定模型
/validate --weights runs/train/exp/weights/best.pt
```

## 輸出指標

- **mAP@0.5**: 0.5 IOU 閾值下的平均精度
- **mAP@0.5:0.95**: 多個 IOU 閾值下的平均精度
- **Precision**: 精確率
- **Recall**: 召回率
- **F1-Score**: F1 分數

驗證結果儲存在 runs/val/exp/
