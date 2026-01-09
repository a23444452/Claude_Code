# 啟動 YOLO 模型訓練

快速啟動 YOLO 模型訓練流程，自動檢查環境並開始訓練。

## 執行步驟

1. 檢查資料集是否已預處理（dataset/MBB_gray_processed/）
2. 檢查配置檔是否存在（config/data_gray.yaml）
3. 啟動訓練，使用以下預設參數：
   - 模型：yolo11n
   - Epochs：100
   - Batch size：8
   - 啟用資料增強
4. 顯示訓練指令和預期輸出位置

## 使用範例

```bash
# 使用預設參數
/train

# 或指定參數
/train --epochs 50 --batch 4
```

## 注意事項

- 訓練前確認資料集已正確預處理
- 訓練結果將儲存在 runs/train/exp/
- 如果記憶體不足，請降低 batch size
