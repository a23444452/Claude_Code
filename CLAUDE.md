# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
基於 YOLO11n 的即時物件偵測系統，包含完整的資料處理、訓練、推論與 Web 介面。

## Tech Stack
- **Core**: Python 3.10+, PyTorch 2.9.1, Ultralytics YOLO11n
- **Backend**: FastAPI 0.104.1, Uvicorn (ASGI server)
- **Frontend**: Vanilla JavaScript + Canvas API (無框架依賴)
- **加速**: Apple Silicon MPS / NVIDIA CUDA

## Architecture Overview

### 三層架構設計
1. **前端層** (port 3000): 純 JavaScript SPA，使用 Canvas 即時繪製偵測結果
2. **API 層** (port 8000): FastAPI REST API，處理圖片上傳與推論請求
3. **模型層**: YOLO11n (2.59M 參數) 執行物件偵測，支援 MPS/CUDA 加速

### 關鍵設計決策
- **單 API 檔案設計**: `src/api/main.py` 包含所有端點，便於維護小型專案
- **模型啟動載入**: 使用 FastAPI `@app.on_event("startup")` 確保模型只載入一次
- **CORS 全開**: 開發環境允許所有來源，生產環境需修改 `allow_origins`
- **MPS 優先**: 訓練腳本自動偵測 MPS > CUDA > CPU
- **無資料庫**: 所有結果即時回傳，不儲存歷史記錄

### 資料流程
```
原始資料 → preprocess.py (驗證+切分) → train.py (訓練) → runs/train/exp/weights/best.pt
使用者上傳 → FastAPI → YOLO 推論 → JSON 結果 → Canvas 繪製
```

## Common Development Commands

### 快速啟動 (推薦使用 Claude Code Commands)
```bash
# 使用 Claude Code commands (自動檢查環境)
/start-services          # 啟動 API + 前端
/project-status          # 檢查專案狀態
/train                   # 開始訓練
/validate                # 驗證模型效能
/api-test                # 測試 API 端點

# 或使用原始命令
./start_all.sh           # 啟動所有服務
./stop_all.sh            # 停止所有服務
python3 check_services.py # 檢查服務狀態
```

### 資料處理工作流程
```bash
# 1. 預處理原始資料集
python src/utils/preprocess.py \
  --source dataset/raw_dataset \
  --output dataset/processed \
  --train-ratio 0.8

# 2. 驗證處理結果
python scripts/validate_dataset.py dataset/processed
```

### 訓練工作流程
```bash
# 測試環境 (快速檢查 MPS/CUDA)
python src/training/train.py --mode test

# 開始訓練
python src/training/train.py \
  --mode train \
  --data config/data.yaml \
  --epochs 100 \
  --batch 8 \
  --augment

# 驗證模型
python src/training/train.py \
  --mode validate \
  --weights runs/train/exp/weights/best.pt \
  --data config/data.yaml

# 訓練結果位置: runs/train/exp/weights/best.pt
```

### API 開發工作流程
```bash
# 啟動開發伺服器 (支援熱重載)
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 生產模式 (多 worker)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

# 測試 API
python src/api/test_api.py

# 查看 API 文檔
open http://localhost:8000/docs
```

### 前端開發
```bash
# 啟動前端服務
cd src/frontend && ./start_frontend.sh

# 前端位置
open http://localhost:3000
```

### 測試與驗證
```bash
# 執行單元測試
pytest tests/

# 測試單一檔案
pytest tests/test_api.py -v

# 檢查代碼覆蓋率
pytest --cov=src tests/
```

## Python Development Standards
- 遵循 PEP8 規範
- 必須使用 Type Hints
- 函數和類別需要 docstring (支援 IDE 自動完成)
- 使用有意義的變數名稱

## Important File Locations

### 模型與配置
- **訓練好的模型**: `runs/train/exp/weights/best.pt` (API 啟動時載入此檔)
- **資料集配置**: `config/data.yaml` (需從 `config/data.example.yaml` 複製並修改路徑)
- **預訓練模型**: `yolo11n.pt` (專案根目錄，首次訓練時自動下載)

### 核心程式碼
- **API 主檔案**: `src/api/main.py` (所有 REST 端點定義於此)
- **訓練腳本**: `src/training/train.py` (包含 MPS 偵測與訓練邏輯)
- **資料預處理**: `src/utils/preprocess.py` (YOLO 格式驗證與資料集切分)
- **前端入口**: `src/frontend/index.html` + `src/frontend/app.js`

### 開發工具
- **Claude Code Commands**: `.claude/commands/*.md` (10 個自訂命令)
- **Claude Code Hooks**: `.claude/hooks/*.py` (4 個驗證 hooks)
- **服務檢查**: `check_services.py` (檢查 API 與前端狀態)
- **啟動腳本**: `start_all.sh` / `stop_all.sh`

### AI Agent 系統
- **Agent 定義**: `.agents/*.md` (37 個專業領域 Agent)
- **Agent 名錄**: `README_AGENTS.md` (完整 Agent 清單與使用說明)
- **會議主持**: `PROMPT_MEETING_SETUP.md` (多 Agent 協作模板)

## Git Workflow & Rules

### 重要：自動驗證 Hooks
專案配置了 Git commit 驗證 hook，會在 commit 前自動阻止以下檔案：
- ❌ 模型檔案 (`*.pt`)
- ❌ 資料集圖片與標註 (`dataset/`)
- ❌ 本地配置檔 (`config/*.yaml` 非 example)
- ❌ 大型檔案 (>10MB)
- ❌ 敏感資訊 (`.env`)

Hook 位置: `.claude/hooks/git_commit_validator.py`

### 絕對不可 Commit 的內容
1. **模型權重** (`*.pt`, `models/`) - 檔案過大，使用 Git LFS 或雲端儲存
2. **資料集** (`dataset/`) - 包含圖片與標註，使用 DVC 管理
3. **本地配置** (`config/*.yaml`) - 每個開發者路徑不同，只 commit `*.example.yaml`
4. **訓練輸出** (`runs/`, `wandb/`) - 自動生成的大量檔案
5. **Plugin 輸出** (`analysis/`, `monitoring/`, `optimization/`, `security/`) - 自動生成報告
6. **敏感資訊** (`.env`, API keys, tokens, passwords)

### 應該 Commit 的內容
- ✅ 程式碼 (`.py`, `.js`, `.html`, `.css`)
- ✅ 文檔 (`.md`)
- ✅ 配置範本 (`config.example.yaml`)
- ✅ 依賴清單 (`requirements.txt`)
- ✅ 測試檔案 (`test_*.py`)
- ✅ CI/CD 配置 (`.github/workflows/`)
- ✅ Claude Code 設定 (`.claude/`)

### Commit Message 規範
遵循 Conventional Commits，所有 commit 必須包含 Co-Authored-By：
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:** `feat` (新功能) | `fix` (錯誤修復) | `docs` (文檔) | `style` (格式) | `refactor` (重構) | `test` (測試) | `chore` (工具) | `perf` (效能)

**範例:**
```bash
git commit -m "$(cat <<'EOF'
feat(api): add batch prediction endpoint

Implement /predict/batch for processing multiple images.
- Support up to 10 images per request
- Add input validation

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 快速 Git 工作流程
```bash
# 使用 Claude Code command (推薦)
/commit-push

# 或手動執行
git add <files>
git commit -m "message"
git push
```

## Documentation Update Rules

### 何時更新文檔
當進行以下變更時，必須同步更新對應文檔：
- **新增/修改功能** → 更新 `README.md` 功能說明與使用範例
- **新增/修改 API 端點** → 更新 `README.md` API 文檔表格
- **架構變更** → 更新 `ARCHITECTURE.md`
- **工作流程變更** → 更新 `USAGE.md`
- **新增 Claude Code command/plugin** → 更新對應的 README
- **依賴變更** → 更新 `README.md` 系統要求與安裝步驟

### 文檔檔案對應
- `README.md` - 專案總覽、快速開始、API 文檔
- `ARCHITECTURE.md` - 系統架構、技術棧、設計決策
- `USAGE.md` - 詳細使用指南、工作流程
- `.claude/commands/*.md` - Claude Code 命令說明
- `.claude/plugins/*/README.md` - Plugin 功能與使用方式

### 文檔風格
- 使用繁體中文撰寫（保持專案一致性）
- 提供可執行的程式碼範例
- 包含預期輸出範例
- 重要指令用程式碼區塊標示
