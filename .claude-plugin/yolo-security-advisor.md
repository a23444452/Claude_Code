# YOLO Security Advisor Plugin

## Description
YOLO API 安全顧問，提供安全最佳實踐，防止常見漏洞（檔案上傳攻擊、DoS、資料洩漏等）。

## Security Checklist

### 檔案上傳安全
- ✅ 驗證檔案類型（MIME type）
- ✅ 限制檔案大小（< 10MB）
- ✅ 掃描惡意檔案
- ✅ 使用臨時目錄
- ✅ 自動清理上傳檔案

### API 安全
- ✅ 實作速率限制（Rate Limiting）
- ✅ 輸入驗證
- ✅ 錯誤訊息不洩漏資訊
- ✅ CORS 配置
- ✅ HTTPS 強制

### 資料保護
- ✅ 不記錄敏感資訊
- ✅ 預測結果脫敏
- ✅ 圖片自動刪除

## Example: Secure File Upload
```python
from fastapi import UploadFile, HTTPException
import magic

ALLOWED_TYPES = ["image/jpeg", "image/png"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@app.post("/predict")
async def predict(file: UploadFile):
    # 1. 檢查檔案大小
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")

    # 2. 驗證 MIME type
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")

    # 3. 處理...
    results = model.predict(content)

    return {"detections": results}
```

## Version History
- v1.0.0: 初始版本
