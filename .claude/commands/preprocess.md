# 資料預處理

執行 YOLO 資料集預處理流程，包括驗證、轉換和切分。

## 執行步驟

1. 檢查原始資料集路徑
2. 執行預處理腳本：
   - 驗證圖片完整性
   - RGB 格式轉換
   - 標註檔驗證
   - Train/Val 切分（預設 80/20）
3. 生成 classes.txt
4. 顯示處理統計資訊

## 使用範例

```bash
# 使用預設路徑
/preprocess

# 指定來源和輸出
/preprocess --source dataset/my_dataset --output dataset/my_dataset_processed
```

## 輸出

預處理後的資料集結構：
```
dataset/processed/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── classes.txt
```
