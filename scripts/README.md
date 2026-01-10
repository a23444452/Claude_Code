# YOLO Project Scripts

本目錄包含專案的實用腳本工具，協助開發、部署、維護工作流程。

## 📋 目錄

- [腳本列表](#腳本列表)
- [使用指南](#使用指南)
- [常見使用場景](#常見使用場景)
- [疑難排解](#疑難排解)

---

## 📜 腳本列表

### 🐳 DevContainer 相關

#### 1. `run_devcontainer.ps1` (Windows)
**用途**: 在 Windows 上啟動 DevContainer 並執行 Claude Code

**語法**:
```powershell
.\scripts\run_devcontainer.ps1 [-Backend docker|podman] [-SkipClaude]
```

**參數**:
- `-Backend`: 容器後端 (docker 或 podman)，預設 docker
- `-SkipClaude`: 跳過 Claude Code 自動啟動

**範例**:
```powershell
# 使用 Docker (預設)
.\scripts\run_devcontainer.ps1

# 使用 Podman
.\scripts\run_devcontainer.ps1 -Backend podman

# 不啟動 Claude Code
.\scripts\run_devcontainer.ps1 -SkipClaude
```

**前置需求**:
- Docker Desktop 或 Podman
- DevContainer CLI: `npm install -g @devcontainers/cli`
- PowerShell 5.0+

---

#### 2. `run_devcontainer.sh` (macOS/Linux)
**用途**: 在 macOS/Linux 上啟動 DevContainer 並執行 Claude Code

**語法**:
```bash
bash scripts/run_devcontainer.sh [OPTIONS]
```

**選項**:
- `-b, --backend`: 容器後端 (docker 或 podman)
- `-s, --skip-claude`: 跳過 Claude Code 自動啟動
- `-h, --help`: 顯示幫助訊息

**範例**:
```bash
# 使用 Docker (預設)
bash scripts/run_devcontainer.sh

# 使用 Podman
bash scripts/run_devcontainer.sh --backend podman

# 不啟動 Claude Code
bash scripts/run_devcontainer.sh --skip-claude
```

**前置需求**:
- Docker Desktop 或 Podman
- DevContainer CLI: `npm install -g @devcontainers/cli`
- Bash 4.0+

---

### ⚙️ 專案設定

#### 3. `setup_project.sh`
**用途**: 初始化專案結構和安裝依賴

**語法**:
```bash
bash scripts/setup_project.sh
```

**功能**:
- ✅ 檢查 Python 和 pip 安裝
- ✅ 建立專案目錄結構
- ✅ 建立 Python package 檔案 (`__init__.py`)
- ✅ 複製 `.env` 範例檔案
- ✅ 安裝 Python 依賴 (從 `requirements.txt`)
- ✅ 下載預設 YOLO 模型 (`yolo11n.pt`)
- ✅ 初始化 Git repository
- ✅ 設定 Git pre-commit hook
- ✅ 建立範例程式碼檔案

**範例**:
```bash
# 完整設定
bash scripts/setup_project.sh
```

**建立的目錄結構**:
```
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/
models/
runs/
logs/
config/
src/
├── api/
├── training/
├── data/
└── utils/
tests/
analysis/
monitoring/
optimization/
security/
```

**建立的範例檔案**:
- `src/training/train.py` - 訓練腳本範例
- `src/api/main.py` - FastAPI 應用程式範例
- `tests/test_model.py` - 測試範例

**注意事項**:
- 如果 `requirements.txt` 不存在，會安裝基本套件
- Git hook 會防止提交 `.pt` 模型檔案和大檔案
- `.env` 檔案需要手動編輯 API keys

---

### 📦 模型管理

#### 4. `download_models.sh`
**用途**: 下載官方 YOLO 模型

**語法**:
```bash
bash scripts/download_models.sh [models...]
bash scripts/download_models.sh --all
```

**模型變體**:
| 模型 | 大小 | 參數量 | mAP | 速度 | 適用場景 |
|------|------|--------|-----|------|----------|
| n | 6MB | 2.6M | 39.5% | 1.5ms | 邊緣裝置、即時應用 |
| s | 22MB | 9.4M | 47.0% | 2.3ms | 一般用途 |
| m | 50MB | 20.1M | 51.5% | 4.5ms | 平衡準確度和速度 |
| l | 58MB | 25.3M | 53.4% | 6.5ms | 高準確度需求 |
| x | 138MB | 56.9M | 54.7% | 10.6ms | 最高準確度 |

**範例**:
```bash
# 互動模式 (會提示選擇)
bash scripts/download_models.sh

# 下載單一模型
bash scripts/download_models.sh n

# 下載多個模型
bash scripts/download_models.sh n s m

# 下載所有模型
bash scripts/download_models.sh --all
```

**模型選擇建議**:
- **邊緣裝置** (Raspberry Pi): `n`
- **即時應用** (監控系統): `n` 或 `s`
- **一般用途** (大多數情況): `s` 或 `m`
- **高準確度** (品質檢測): `l` 或 `x`
- **伺服器部署**: `m` 或 `l`

**下載位置**:
- 模型會複製到 `models/` 目錄
- 也會在專案根目錄保留一份

---

### 🧹 清理工具

#### 5. `cleanup.sh`
**用途**: 清理臨時檔案、快取和生成的輸出

**語法**:
```bash
bash scripts/cleanup.sh [OPTIONS]
```

**選項**:
- `--aggressive`: 深度清理 (包含日誌和 plugin 輸出)
- `--dry-run`: 預覽將被刪除的檔案 (不實際刪除)
- `--remove-models`: 也刪除下載的模型 (危險！)
- `-h, --help`: 顯示幫助訊息

**清理項目**:

**基本清理**:
- Python 快取 (`__pycache__/`, `*.pyc`, `*.pyo`)
- pytest 快取 (`.pytest_cache/`, `.coverage`)
- mypy 快取 (`.mypy_cache/`)
- 臨時檔案 (`tmp/`, `*.tmp`, `*~`)
- macOS `.DS_Store` 檔案

**訓練輸出** (需確認):
- `runs/` 目錄 (所有訓練執行記錄)

**深度清理** (`--aggressive`):
- Plugin 輸出 (`analysis/`, `monitoring/`, `optimization/`, `security/`)
- 日誌檔案 (`logs/`, `*.log`)

**模型** (`--remove-models`):
- 所有 `.pt` 模型檔案 (需二次確認)

**範例**:
```bash
# 基本清理
bash scripts/cleanup.sh

# 預覽清理 (不實際刪除)
bash scripts/cleanup.sh --dry-run

# 深度清理
bash scripts/cleanup.sh --aggressive

# 完整清理 (包含模型)
bash scripts/cleanup.sh --aggressive --remove-models
```

**清理後資訊**:
- 顯示節省的磁碟空間
- 可選 Docker 快取清理

**安全性**:
- 刪除 `runs/` 和模型前會要求確認
- `--dry-run` 模式安全預覽
- 不會刪除原始資料集

---

### ✅ 驗證工具

#### 6. `validate_dataset.py`
**用途**: 驗證 YOLO 格式資料集的正確性

**語法**:
```bash
python scripts/validate_dataset.py config/data.yaml [-v]
```

**選項**:
- `-v, --verbose`: 顯示詳細資訊 (包含錯誤列表)

**驗證項目**:

✅ **配置檢查**:
- 檢查 `data.yaml` 存在
- 驗證必要欄位 (path, train, val, names, nc)

✅ **路徑檢查**:
- 驗證基礎路徑存在
- 驗證訓練/驗證集路徑存在

✅ **圖片檢查**:
- 計算圖片數量
- 檢查對應的標註檔案是否存在

✅ **標註檢查**:
- 驗證檔案格式 (每行 5 個值)
- 檢查 class ID 範圍 (0 到 nc-1)
- 檢查座標範圍 (0 到 1)
- 檢查寬高有效性 (> 0)

✅ **類別分布分析**:
- 顯示每個類別的樣本數量
- 計算百分比
- 視覺化分布 (長條圖)
- 偵測類別不平衡

**輸出範例**:
```
Class Distribution (Training Set):
──────────────────────────────────────────────────
helmet          |   850 ( 68.0%) ████████████████████████████████
no_helmet       |   400 ( 32.0%) ████████████████
──────────────────────────────────────────────────
Total           |  1250

⚠ Class imbalance detected (ratio: 2.1:1)
ℹ Consider data augmentation or weighted loss
```

**範例**:
```bash
# 基本驗證
python scripts/validate_dataset.py config/data.yaml

# 詳細驗證
python scripts/validate_dataset.py config/data.yaml --verbose
```

**使用時機**:
- 📌 訓練前必須執行
- 📌 新增資料後驗證
- 📌 修改標註後確認
- 📌 資料集整合後檢查

**常見問題**:

❌ **Missing label files**:
- 原因: 圖片沒有對應的 `.txt` 標註檔案
- 解決: 使用標註工具補充標註

❌ **Invalid class ID**:
- 原因: 標註檔案中的 class ID 超出範圍
- 解決: 檢查 `data.yaml` 的 `nc` 設定是否正確

❌ **Coordinates out of range**:
- 原因: 座標值不在 0-1 範圍內
- 解決: 重新匯出標註，確保使用 YOLO 格式

❌ **Class imbalance**:
- 原因: 某些類別樣本過少
- 解決: 收集更多資料或使用資料增強

---

## 🚀 使用指南

### 首次設定專案

```bash
# 1. Clone 專案
git clone https://github.com/a23444452/Claude_Code.git YOLO_Project
cd YOLO_Project

# 2. 設定專案結構
bash scripts/setup_project.sh

# 3. 編輯環境變數
nano .env

# 4. 下載 YOLO 模型
bash scripts/download_models.sh n s

# 5. 準備資料集
# ... 將圖片和標註放到 dataset/ 目錄 ...

# 6. 驗證資料集
python scripts/validate_dataset.py config/data.yaml -v

# 7. 開始訓練
python src/training/train.py
```

### 使用 DevContainer 開發

**Windows**:
```powershell
# 啟動 DevContainer
.\scripts\run_devcontainer.ps1

# 容器內執行
/train
/api-test
```

**macOS/Linux**:
```bash
# 啟動 DevContainer
bash scripts/run_devcontainer.sh

# 容器內執行
/train
/api-test
```

### 定期維護

```bash
# 清理臨時檔案
bash scripts/cleanup.sh

# 深度清理 (每月一次)
bash scripts/cleanup.sh --aggressive

# 預覽清理內容
bash scripts/cleanup.sh --dry-run
```

---

## 📖 常見使用場景

### 場景 1: 新專案快速啟動

```bash
# 一鍵設定
bash scripts/setup_project.sh

# 下載需要的模型
bash scripts/download_models.sh n s

# 編輯配置
cp config/data.example.yaml config/data.yaml
nano config/data.yaml
```

### 場景 2: 訓練前準備

```bash
# 驗證資料集
python scripts/validate_dataset.py config/data.yaml -v

# 如果有錯誤，修正後再次驗證
python scripts/validate_dataset.py config/data.yaml

# 開始訓練
/train
```

### 場景 3: 切換模型大小

```bash
# 下載新模型
bash scripts/download_models.sh m

# 在訓練腳本中修改
# model = YOLO('models/yolo11m.pt')
```

### 場景 4: 清理磁碟空間

```bash
# 檢查將被清理的內容
bash scripts/cleanup.sh --dry-run

# 執行清理
bash scripts/cleanup.sh --aggressive

# 清理 Docker 快取 (選擇 y)
```

### 場景 5: DevContainer 開發

```bash
# 方法 1: VS Code
# F1 → Dev Containers: Reopen in Container

# 方法 2: 使用腳本
bash scripts/run_devcontainer.sh

# 容器內工作
claude
/dataset-analyzer --dataset dataset/my_dataset
```

---

## 🔧 疑難排解

### 問題: run_devcontainer.sh 無法執行

**錯誤**: `permission denied`

**解決**:
```bash
chmod +x scripts/run_devcontainer.sh
bash scripts/run_devcontainer.sh
```

### 問題: setup_project.sh 找不到 pip

**錯誤**: `pip: command not found`

**解決**:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3-pip

# Windows
# 從 python.org 下載並安裝 Python
```

### 問題: download_models.sh 下載失敗

**錯誤**: `Failed to download`

**解決**:
```bash
# 檢查網路連線
ping github.com

# 檢查 ultralytics 安裝
pip install --upgrade ultralytics

# 手動下載
python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
```

### 問題: validate_dataset.py 找不到模組

**錯誤**: `ModuleNotFoundError: No module named 'yaml'`

**解決**:
```bash
pip install pyyaml
```

### 問題: cleanup.sh 刪除後無法復原

**解決**:
```bash
# 總是先用 --dry-run 預覽
bash scripts/cleanup.sh --dry-run

# 確認後再執行
bash scripts/cleanup.sh
```

---

## 💡 最佳實踐

### 1. 訓練前流程

```bash
# 完整檢查
python scripts/validate_dataset.py config/data.yaml -v

# 使用適合的模型
bash scripts/download_models.sh n  # 快速測試
bash scripts/download_models.sh m  # 正式訓練

# 記錄實驗
/train --epochs 100 --batch 16
```

### 2. 定期維護

```bash
# 每週
bash scripts/cleanup.sh

# 每月
bash scripts/cleanup.sh --aggressive

# 訓練完成後
# 保留最佳模型，清理中間結果
```

### 3. 團隊協作

```bash
# 新成員加入
bash scripts/setup_project.sh

# 共享配置
git add config/data.example.yaml
git commit -m "docs: add data config example"

# 不共享
# - .env (敏感資訊)
# - 模型檔案 (太大)
# - 資料集 (版權)
```

### 4. DevContainer 使用

```bash
# 首次使用
bash scripts/run_devcontainer.sh

# 容器內開發
claude
/train
/api-test

# 退出容器
exit

# 清理容器
docker stop <container_id>
devcontainer down --workspace-folder .
```

---

## 📚 相關資源

### 專案文檔
- [README.md](../README.md) - 專案總覽
- [CLAUDE.md](../CLAUDE.md) - 開發規範
- [.devcontainer/README.md](../.devcontainer/README.md) - Dev Container 文檔
- [.github/README.md](../.github/README.md) - GitHub 工具

### 工具文檔
- [DevContainer CLI](https://github.com/devcontainers/cli)
- [Ultralytics YOLO](https://docs.ultralytics.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## 🤝 貢獻

歡迎改進這些腳本工具！

**建議改進**:
- 新增更多實用腳本
- 改進錯誤處理
- 增加進度顯示
- 支援更多平台
- 改善文檔

請提交 Pull Request 或建立 Issue。

---

## 📝 授權

此腳本集合遵循專案授權條款。

---

**享受自動化的開發體驗！** 🎉

如有問題或建議，歡迎在 [GitHub Issues](https://github.com/a23444452/Claude_Code/issues) 留言。
