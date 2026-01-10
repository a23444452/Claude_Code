# API 除錯助手提示模板

## 用途
協助診斷和解決 FastAPI 後端相關的問題，包括啟動失敗、端點錯誤、效能問題等。

## 使用方式
將此提示模板貼到 Claude Code 中，並替換 `[...]` 中的內容為你的實際資訊。

---

## 提示模板

```
我的 FastAPI API 遇到問題，需要協助除錯。

### 環境資訊
- Python 版本: [例如: 3.10.5]
- FastAPI 版本: [版本號]
- Uvicorn 版本: [版本號]
- Ultralytics 版本: [版本號]
- 作業系統: [macOS/Linux/Windows]
- 裝置: [CPU/MPS/CUDA]

### 問題描述
[詳細描述問題]
- 問題類型: [無法啟動/端點錯誤/效能問題/CORS/其他]
- 相關端點: [例如: POST /predict]
- 何時發生: [一直/偶爾/特定情況下]

### 錯誤訊息/API 日誌
```
[貼上完整的錯誤訊息或 API 日誌]
```

### 請求範例
```bash
[貼上發送的請求，例如 curl 命令或程式碼]
```

### 實際回應
```json
[貼上 API 的實際回應]
```

### 預期回應
```json
[描述預期的回應格式]
```

### 相關程式碼片段
```python
[如果有相關的程式碼，請貼在這裡]
```

### 已嘗試的解決方法
1. ...
2. ...

請幫我：
1. 診斷問題根本原因
2. 提供解決方案和程式碼修正
3. 建議如何預防類似問題
4. 如果是效能問題，提供優化建議

如需進行 API 測試，請使用：`/api-test`
如需安全性檢查，請使用：`/api-security`
```

---

## 常見問題範例

### 1. API 啟動失敗
```
我的 FastAPI API 遇到問題，需要協助除錯。

### 環境資訊
- Python 版本: 3.10.5
- FastAPI 版本: 0.104.1
- Uvicorn 版本: 0.24.0
- 作業系統: macOS

### 問題描述
API 無法啟動，顯示模型載入錯誤。

### 錯誤訊息
```
INFO:     Started server process [12345]
ERROR:    Exception in ASGI application
FileNotFoundError: [Errno 2] No such file or directory: 'models/best.pt'
```

請幫我解決這個問題。
```

### 2. 端點回應錯誤
```
我的 FastAPI API 遇到問題，需要協助除錯。

### 問題描述
POST /predict 端點回傳 500 錯誤

### 請求範例
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test.jpg" \
  -F "conf_threshold=0.25"
```

### 實際回應
```json
{
  "detail": "Internal Server Error"
}
```

### API 日誌
```
ERROR: Exception in predict endpoint: 'NoneType' object has no attribute 'shape'
```

請協助診斷問題。
```

### 3. 效能問題
```
我的 FastAPI API 遇到問題，需要協助除錯。

### 問題描述
API 回應時間很慢，每次請求需要 5-10 秒

### 環境資訊
- 裝置: Apple Silicon M1
- 模型: yolo11n.pt
- 並發請求: 1

### 效能資訊
- 回應時間: 7000ms
- 記憶體使用: 3GB
- CPU 使用率: 45%

### 相關程式碼片段
```python
@app.post("/predict")
async def predict(file: UploadFile):
    model = YOLO("yolo11n.pt")  # 每次都重新載入
    image = await file.read()
    results = model.predict(image)
    return results
```

請提供效能優化建議。
```

---

## API 測試流程

### 基本測試步驟
1. 使用 `/api-test` 命令測試所有端點
2. 檢查 Swagger UI: http://localhost:8000/docs
3. 查看 API 日誌輸出
4. 使用 `/api-security` 進行安全性檢查

### 常用除錯命令
```bash
# 查看 API 日誌
tail -f logs/api.log

# 測試健康檢查端點
curl http://localhost:8000/health

# 測試模型資訊端點
curl http://localhost:8000/model/info

# 測試預測端點
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test.jpg" \
  -F "conf_threshold=0.25"
```

---

## 提示技巧

1. **完整錯誤日誌**: 包含完整的 traceback 和錯誤訊息
2. **請求內容**: 提供實際發送的請求（curl/程式碼）
3. **環境資訊**: 說明 Python、FastAPI、依賴版本
4. **重現步驟**: 描述如何重現問題
5. **相關程式碼**: 貼上相關的 API 端點程式碼
6. **使用工具**: 配合 `/api-test` 和 `/api-security` 命令
