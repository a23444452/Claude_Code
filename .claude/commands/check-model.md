# 檢查模型狀態

檢查訓練好的 YOLO 模型狀態和效能指標。

## 執行步驟

1. 查找最新訓練的模型（runs/train/exp*/weights/best.pt）
2. 顯示模型資訊：
   - 檔案大小
   - 類別數量
   - 訓練參數
3. 如果存在 results.png，顯示訓練曲線路徑
4. 檢查模型是否已載入到 API

## 使用範例

```bash
# 檢查最新模型
/check-model

# 檢查指定模型
/check-model --weights runs/train/exp/weights/best.pt
```

## 顯示資訊

- 模型路徑和大小
- 訓練配置
- 效能指標（如果有）
- API 載入狀態
