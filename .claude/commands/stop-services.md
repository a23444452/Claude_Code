# 停止所有服務

停止正在運行的 YOLO 專案服務（API + Frontend）。

## 執行步驟

1. 查找正在運行的 uvicorn 進程（port 8000）
2. 查找正在運行的 http.server 進程（port 3000）
3. 安全地終止所有相關進程
4. 確認服務已停止

## 使用範例

```bash
# 停止所有服務
/stop-services
```

## 檢查項目

- API 服務狀態（port 8000）
- 前端服務狀態（port 3000）
- 清理殘留進程
