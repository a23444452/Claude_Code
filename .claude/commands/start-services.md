# 啟動所有服務

一鍵啟動 YOLO 專案的所有服務（API + Frontend）。

## 執行步驟

1. 檢查是否已有服務在運行（避免端口衝突）
2. 在背景啟動 FastAPI 後端（port 8000）
3. 在背景啟動前端服務（port 3000）
4. 等待服務啟動完成
5. 顯示服務狀態和訪問 URL

## 使用範例

```bash
# 啟動所有服務
/start-services
```

## 服務資訊

啟動後可訪問：
- **前端 UI**: http://localhost:3000
- **API 文檔**: http://localhost:8000/docs
- **健康檢查**: http://localhost:8000/health

## 停止服務

使用 `/stop-services` 或執行：
```bash
./stop_all.sh
```
