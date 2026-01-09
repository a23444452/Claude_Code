# 測試 API 端點

全面測試 FastAPI 後端的所有端點，確保服務正常運作。

## 執行步驟

1. 檢查 API 服務是否啟動（http://localhost:8000/health）
2. 測試所有端點：
   - GET /health - 健康檢查
   - GET /model/info - 模型資訊
   - POST /predict - 單張圖片偵測（使用測試圖片）
3. 顯示測試結果和回應時間
4. 如果 API 未啟動，提供啟動指令

## 使用範例

```bash
# 測試所有端點
/api-test

# 指定測試圖片
/api-test --image path/to/test.jpg
```

## 測試項目

- API 可用性
- 回應時間
- 錯誤處理
- 結果格式正確性
