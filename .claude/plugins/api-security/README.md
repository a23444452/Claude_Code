# API Security Plugin

FastAPI 後端安全性檢查工具，掃描常見漏洞並提供修復建議。

## 功能特色

### 🔒 安全檢查
- OWASP Top 10 漏洞掃描
- 輸入驗證檢查
- 認證與授權檢查
- CORS 配置審查
- Rate limiting 檢查

### 🛡️ 程式碼審查
- SQL Injection 風險
- XSS 攻擊向量
- Path Traversal 漏洞
- Command Injection 檢查
- 敏感資訊洩漏

### 📝 配置審查
- 環境變數使用
- Secret 管理
- HTTPS 強制
- 安全標頭設定
- 錯誤訊息洩漏

### 🔍 依賴檢查
- 過期套件掃描
- 已知漏洞檢測
- 許可證合規性
- 安全更新建議

## 使用方式

### 命令
```bash
# 執行完整安全掃描
/api-security

# 僅檢查程式碼
/api-security --code-only

# 僅檢查配置
/api-security --config-only

# 生成詳細報告
/api-security --detailed
```

### 輸出範例

```
=== API 安全性檢查報告 ===

🔍 掃描範圍: src/api/

📊 檢查摘要:
  總檢查項: 25
  通過: 18 ✓
  警告: 5 ⚠️
  嚴重: 2 ✗

🔒 認證與授權:
  ✓ 無硬編碼的密碼或 token
  ✗ 缺少 API 認證機制 [HIGH]
  ⚠️ 建議實作 API Key 或 JWT 認證

🛡️ 輸入驗證:
  ✓ 檔案類型驗證 (main.py:45)
  ✓ 檔案大小限制
  ⚠️ 建議增加檔案名稱清理 (防止路徑穿越)
  ⚠️ 建議驗證 conf_threshold 範圍 (0-1)

🌐 CORS 配置:
  ✗ CORS 允許所有來源 "*" [MEDIUM]
  建議: 限制為特定域名

  修復建議:
  origins = [
      "http://localhost:3000",
      "https://yourdomain.com"
  ]

🔐 資料保護:
  ✓ 無 SQL 注入風險 (使用 ORM)
  ✓ 無明顯的 XSS 漏洞
  ⚠️ 上傳檔案未進行病毒掃描
  ⚠️ 建議加密敏感日誌

⚡ Rate Limiting:
  ✗ 缺少請求速率限制 [HIGH]
  建議: 實作 slowapi 或 middleware

  修復範例:
  from slowapi import Limiter
  limiter = Limiter(key_func=get_remote_address)
  @limiter.limit("10/minute")

📦 依賴安全:
  ✓ FastAPI: 0.104.1 (最新)
  ✓ Uvicorn: 0.24.0 (最新)
  ✓ 無已知高危漏洞

🔧 配置安全:
  ✓ 使用環境變數
  ⚠️ 建議使用 .env 檔案管理配置
  ⚠️ 生產環境應關閉 debug 模式

📝 錯誤處理:
  ✓ 全域異常處理器
  ⚠️ 錯誤訊息可能洩漏內部資訊

🎯 安全評分: 72/100 (中等)

優先修復項目:
1. [HIGH] 實作 API 認證機制
2. [HIGH] 添加 Rate Limiting
3. [MEDIUM] 限制 CORS 來源
4. [MEDIUM] 添加檔案掃描
5. [LOW] 改善錯誤訊息處理

💡 快速修復建議:

1. 添加 API Key 認證:
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "your-secret-key"
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
```

2. 添加 Rate Limiting:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(request: Request, ...):
    ...
```

3. 限制 CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 不要用 "*"
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

4. 檔案上傳安全:
```python
import magic
ALLOWED_TYPES = ["image/jpeg", "image/png"]

async def validate_file(file: UploadFile):
    # 檢查副檔名
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png"]:
        raise HTTPException(400, "Invalid file type")

    # 檢查 MIME 類型
    content = await file.read()
    file_type = magic.from_buffer(content, mime=True)
    if file_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file content")

    await file.seek(0)
    return file
```
```

## 檢查項目

### 注入攻擊
- ✅ SQL Injection
- ✅ Command Injection
- ✅ Path Traversal
- ✅ Header Injection

### 認證與授權
- ✅ API Key 實作
- ✅ JWT Token 驗證
- ✅ Session 管理
- ✅ 權限控制

### 輸入驗證
- ✅ 檔案類型驗證
- ✅ 檔案大小限制
- ✅ 參數範圍檢查
- ✅ 特殊字元過濾

### 配置安全
- ✅ CORS 設定
- ✅ HTTPS 使用
- ✅ 安全標頭
- ✅ Debug 模式

### 資料保護
- ✅ 敏感資訊加密
- ✅ 日誌安全
- ✅ 錯誤訊息
- ✅ 檔案儲存

## 配置選項

```json
{
  "severity_levels": {
    "critical": ["authentication", "injection"],
    "high": ["rate_limiting", "cors"],
    "medium": ["file_validation", "error_handling"],
    "low": ["logging", "headers"]
  },
  "checks": {
    "enable_owasp_scan": true,
    "enable_dependency_scan": true,
    "enable_code_review": true,
    "enable_config_review": true
  },
  "ignore_patterns": [
    "*/tests/*",
    "*/venv/*"
  ]
}
```

## OWASP Top 10 對照

| OWASP 風險 | 檢查狀態 | 修復建議 |
|-----------|---------|---------|
| A01: Broken Access Control | ⚠️ 部分 | 添加認證機制 |
| A02: Cryptographic Failures | ✓ 通過 | - |
| A03: Injection | ✓ 通過 | - |
| A04: Insecure Design | ⚠️ 部分 | Rate limiting |
| A05: Security Misconfiguration | ⚠️ 部分 | CORS 限制 |
| A06: Vulnerable Components | ✓ 通過 | - |
| A07: Authentication Failures | ✗ 失敗 | 實作認證 |
| A08: Data Integrity Failures | ✓ 通過 | - |
| A09: Logging Failures | ⚠️ 部分 | 改善日誌 |
| A10: SSRF | ✓ 通過 | - |

## 最佳實踐

### 開發階段
1. 每次修改 API 後運行掃描
2. 修復 CRITICAL 和 HIGH 級別問題
3. 定期更新依賴套件
4. Code review 時參考報告

### 部署前
1. 執行完整掃描
2. 確保評分 > 80
3. 無 CRITICAL 級別問題
4. 配置生產環境設定

### 生產環境
1. 啟用所有安全功能
2. 定期執行掃描
3. 監控異常訪問
4. 保持依賴更新

## 整合建議

```bash
# 開發流程
/api-security              # 檢查安全性
# 修復問題
/api-test                  # 測試功能正常
/commit-push              # 提交變更
```

## 輸出檔案

- `security/scan_report.txt` - 完整掃描報告
- `security/vulnerabilities.json` - 漏洞詳細資訊
- `security/fix_suggestions.md` - 修復建議
- `security/owasp_checklist.md` - OWASP 檢查清單

## 快速修復腳本

插件會生成自動修復建議腳本：
```python
# security/quick_fixes.py
# 執行此腳本可自動應用部分修復

def apply_rate_limiting():
    """添加 rate limiting"""
    ...

def restrict_cors():
    """限制 CORS 來源"""
    ...

def add_api_key_auth():
    """添加 API Key 認證"""
    ...
```

## 持續監控

建議設定 CI/CD 整合：
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run API Security Scan
        run: claude /api-security
      - name: Check score
        run: |
          score=$(cat security/score.txt)
          if [ $score -lt 80 ]; then exit 1; fi
```
