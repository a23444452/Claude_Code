# YOLO Image Recognition Project

## Project Overview
這是一個基於 YOLO (You Only Look Once) 的影像辨識系統。
目標：即時偵測 [你的目標物件，例如：工安帽、瑕疵產品]。

## Tech Stack
- **Core**: Python 3.10+, PyTorch, Ultralytics YOLOv8/v11
- **Backend**: FastAPI, Uvicorn
- **Frontend**: [你的選擇，如 Streamlit 或 React]
- **Deployment**: Docker, Nginx

## Key Directories
- `dataset/` - 原始圖片與標註檔 (YOLO format: *.txt)
- `models/` - 訓練好的權重檔 (*.pt)
- `src/training/` - 訓練與微調腳本
- `src/api/` - 後端 API 程式碼
- `src/frontend/` - 前端介面程式碼

## Development Rules

### Python Style
- 遵循 PEP8 規範
- 必須使用 Type Hints
- 函數和類別需要 docstring
- 使用有意義的變數名稱

### Git Rules

#### 絕對不可 Commit 的內容
1. **模型權重檔案**
   - `*.pt` - 所有 PyTorch 模型檔案
   - `models/` - 模型目錄
   - 原因：檔案過大，應使用 Git LFS 或雲端儲存

2. **資料集目錄**
   - `dataset/` - 完整資料集目錄（包含圖片、標註檔、處理後資料）
   - 原因：資料集通常很大，且可能包含敏感資料
   - 建議：使用 DVC (Data Version Control) 或雲端儲存管理資料集

3. **配置檔案**
   - `config/*.yaml` - 包含本地路徑的配置檔
   - 原因：每個開發者的路徑不同，會造成衝突
   - 建議：提供 `config.example.yaml` 範本，開發者自行複製並修改

4. **訓練輸出**
   - `runs/` - YOLO 訓練結果
   - `wandb/` - Weights & Biases 日誌
   - 原因：自動生成的大量檔案，不需版本控制

5. **Plugin 輸出**
   - `analysis/` - Dataset Analyzer 輸出
   - `monitoring/` - Training Monitor 輸出
   - `optimization/` - Model Optimizer 輸出
   - `security/` - API Security 輸出
   - 原因：自動生成的報告檔案

6. **敏感資訊**
   - `.env` - 環境變數檔案
   - API keys, tokens, passwords
   - 資料庫連線字串

#### 應該 Commit 的內容
- ✅ 程式碼檔案 (`.py`, `.js`, `.html`, `.css`)
- ✅ 文檔檔案 (`.md`)
- ✅ 配置範本 (`config.example.yaml`)
- ✅ Requirements 檔案 (`requirements.txt`)
- ✅ 測試檔案 (`test_*.py`)
- ✅ CI/CD 配置 (`.github/workflows/`)
- ✅ Claude Code 設定 (`.claude/`)

#### Commit Message 規範
遵循 Conventional Commits：
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat`: 新功能
- `fix`: 錯誤修復
- `docs`: 文檔更新
- `style`: 程式碼格式（不影響功能）
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 建置工具或輔助工具
- `perf`: 效能優化

**範例:**
```
feat(api): add batch prediction endpoint

Implement /predict/batch endpoint for processing multiple images.
- Support up to 10 images per request
- Return results in array format
- Add input validation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Testing
- 新增功能需撰寫 `pytest` 測試
- 測試覆蓋率應 > 80%
- 執行測試: `pytest tests/`

### Code Review
- 所有 PR 需經過 review
- 確保通過 CI/CD 檢查
- 使用 `/api-security` 檢查安全性
- 確認無敏感資訊洩漏
