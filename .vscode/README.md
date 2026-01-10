# VS Code 配置說明

本目錄包含 YOLO 專案的 VS Code 工作區配置，提供完整的開發環境設定、除錯配置、任務定義和程式碼片段。

## 📋 目錄

- [檔案說明](#檔案說明)
- [快速開始](#快速開始)
- [推薦擴展](#推薦擴展)
- [除錯配置](#除錯配置)
- [任務列表](#任務列表)
- [程式碼片段](#程式碼片段)
- [鍵盤快捷鍵](#鍵盤快捷鍵)
- [常見問題](#常見問題)

---

## 📄 檔案說明

### 1. `extensions.json`
**用途**: 推薦的 VS Code 擴展清單

**包含 30+ 擴展**:
- 🐍 Python 開發 (Python, Pylance, Black, isort, Flake8, mypy)
- 🧪 測試工具 (Python Test Adapter)
- 🔧 Git 工具 (GitLens, Git History, Git Graph)
- 🐳 容器支援 (Remote Containers, Docker)
- 🤖 AI 輔助 (Claude Code)
- 📝 文件編輯 (YAML, Markdown)
- 🔍 其他工具 (REST Client, Error Lens, Jupyter)

**自動提示**: 開啟專案時 VS Code 會提示安裝這些擴展。

---

### 2. `settings.json`
**用途**: 工作區設定

**主要配置**:

#### Python 設定
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
}
```

#### 程式碼品質
- **Black**: 行長度 100
- **isort**: Black profile
- **Flake8**: 忽略 E203, W503
- **mypy**: 忽略缺少的 imports

#### 檔案排除
- 隱藏 `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`
- 搜尋排除 `runs/`, `dataset/`
- 監控排除大目錄以提升效能

#### 編輯器設定
- 行標尺: 100
- 自動裁剪尾隨空白
- 儲存時格式化
- 整理 imports

---

### 3. `launch.json`
**用途**: 除錯配置

**包含 9 種除錯配置**:

#### 1. Python: Current File
除錯當前開啟的 Python 檔案

**快捷鍵**: `F5`

---

#### 2. Python: Train YOLO Model
除錯訓練腳本

**程式**: `src/training/train.py`

**使用時機**: 訓練過程中遇到錯誤

---

#### 3. Python: FastAPI Debug
除錯 FastAPI 應用

**命令**: `uvicorn src.api.main:app --reload`

**連接埠**: 8000

**使用時機**: API 開發和除錯

---

#### 4. Python: YOLO Predict
除錯預測腳本

**使用時機**: 推論問題排查

---

#### 5. Python: Validate Dataset
除錯資料集驗證

**使用時機**: 資料集格式問題

---

#### 6. Python: Pytest (All Tests)
執行所有測試並產生覆蓋率報告

**覆蓋率**: HTML + Terminal

---

#### 7. Python: Pytest (Current File)
執行當前測試檔案

**快速測試單一檔案**

---

#### 8. Python: Debug with Arguments
自訂參數除錯

**彈性配置命令列參數**

---

#### 9. Docker: Attach to Container
連接到執行中的 Docker 容器

**連接埠**: 5678

**使用時機**: 容器內除錯

---

### 4. `tasks.json`
**用途**: 自動化任務定義

**包含 15+ 任務**:

#### 程式碼品質任務

##### Format Code (Black)
```bash
Cmd+Shift+P → Tasks: Run Task → Format Code (Black)
```
格式化所有 Python 程式碼

##### Sort Imports (isort)
整理 import 順序

##### Lint Code (Flake8)
檢查程式碼風格

##### Type Check (mypy)
靜態型別檢查

##### Code Quality Check (All)
執行所有品質檢查 (預設建置任務)

**快捷鍵**: `Cmd+Shift+B` (macOS) / `Ctrl+Shift+B` (Windows)

---

#### 測試任務

##### Run Tests (pytest)
執行所有測試 (預設測試任務)

**快捷鍵**: `Cmd+Shift+T` (可自訂)

##### Run Tests with Coverage
執行測試並產生覆蓋率報告

---

#### YOLO 任務

##### Validate Dataset
驗證資料集格式和完整性

##### Train YOLO Model
開始訓練

##### Download YOLO Models
下載模型 (n, s)

---

#### API 任務

##### Start FastAPI Server
啟動開發伺服器

**自動重載**: 是

**連接埠**: 8000

##### Open Swagger UI
開啟 API 文檔

**URL**: http://localhost:8000/docs

---

#### 專案管理任務

##### Setup Project
初始化專案結構

##### Cleanup Project
清理臨時檔案 (dry-run)

##### Git: Commit with Claude
使用 Claude Code 提交

---

### 5. `yolo.code-snippets`
**用途**: YOLO 專案程式碼片段

**包含 10+ 片段**:

#### `yolo-train`
完整的訓練腳本模板

```python
from ultralytics import YOLO

def train_model(
    data_config: str = "config/data.yaml",
    model: str = "yolo11n.pt",
    epochs: int = 100,
    ...
):
    ...
```

---

#### `yolo-predict`
預測程式碼

```python
from ultralytics import YOLO

model = YOLO("yolo11n.pt")
results = model.predict(...)
```

---

#### `fastapi-endpoint`
FastAPI 端點模板

---

#### `fastapi-yolo-predict`
完整的 YOLO 預測 API 端點

---

#### `pytest-test`
Pytest 測試函數

---

#### `pytest-fixture`
Pytest fixture

---

#### `yolo-validate`
模型驗證程式碼

---

#### `yolo-export`
模型匯出 (ONNX, TensorRT, etc.)

---

#### `docstring-google`
Google-style docstring

---

#### `yolo-augmentation`
資料增強配置

---

## 🚀 快速開始

### 1. 安裝推薦擴展

開啟專案時，VS Code 會提示:

```
This workspace has extension recommendations.
Would you like to install them?
```

點擊 **Install All** 或手動安裝:

```bash
# 查看推薦擴展
Cmd+Shift+P → Extensions: Show Recommended Extensions
```

---

### 2. 選擇 Python 解釋器

```bash
Cmd+Shift+P → Python: Select Interpreter
```

選擇:
- `.venv/bin/python` (虛擬環境)
- 或系統 Python 3.10+

---

### 3. 執行任務

```bash
Cmd+Shift+P → Tasks: Run Task
```

或使用快捷鍵:
- `Cmd+Shift+B` - 預設建置任務 (Code Quality Check)
- `F5` - 開始除錯

---

### 4. 使用程式碼片段

輸入前綴 + `Tab`:

```python
yolo-train<Tab>  # 展開訓練腳本模板
yolo-predict<Tab>  # 展開預測程式碼
```

---

## 📦 推薦擴展詳細說明

### 🐍 Python 開發核心

#### Python (ms-python.python)
- IntelliSense
- 除錯支援
- Linting
- 測試整合

#### Pylance (ms-python.vscode-pylance)
- 快速 IntelliSense
- 型別檢查
- 自動匯入

#### Black Formatter (ms-python.black-formatter)
- 自動格式化
- 儲存時執行

#### isort (ms-python.isort)
- 整理 imports
- Black 整合

#### Flake8 (ms-python.flake8)
- 即時 linting
- 問題面板顯示

#### mypy Type Checker (ms-python.mypy-type-checker)
- 靜態型別檢查
- 錯誤預防

---

### 🧪 測試工具

#### Python Test Adapter (littlefoxteam.vscode-python-test-adapter)
- 測試瀏覽器
- 單獨執行測試
- 除錯測試

---

### 🔧 Git 工具

#### GitLens (eamodio.gitlens)
- Git blame annotations
- 檔案歷史
- 比較工具

#### Git History (donjayamanne.githistory)
- 視覺化 commit 歷史
- 檔案歷史查看

#### Git Graph (mhutchie.git-graph)
- 圖形化 Git 歷史
- 分支視覺化

---

### 🐳 容器支援

#### Remote - Containers (ms-vscode-remote.remote-containers)
- DevContainer 支援
- 容器內開發

#### Docker (ms-azuretools.vscode-docker)
- Dockerfile 語法支援
- 容器管理
- 映像管理

---

### 🤖 AI 輔助

#### Claude Code (anthropic.claude-code)
- AI 程式碼建議
- 智能重構
- 問題解答

---

### 📝 文件編輯

#### YAML (redhat.vscode-yaml)
- YAML 語法支援
- Schema 驗證
- 自動完成

#### Markdown All in One (yzhang.markdown-all-in-one)
- Markdown 預覽
- 鍵盤快捷鍵
- TOC 自動產生

---

### 🔍 其他實用工具

#### REST Client (humao.rest-client)
- 在 VS Code 內測試 API
- 儲存請求歷史

**使用方式**:
建立 `.http` 或 `.rest` 檔案:

```http
### Test YOLO API
POST http://localhost:8000/predict
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="test.jpg"

< ./test.jpg
------WebKitFormBoundary--
```

#### Error Lens (usernamehw.errorlens)
- 行內顯示錯誤
- 即時反饋

#### Jupyter (ms-toolsai.jupyter)
- Notebook 支援
- 互動式開發

---

## 🐛 除錯配置使用指南

### 除錯訓練腳本

1. 開啟 `src/training/train.py`
2. 設定中斷點 (行號左側點擊)
3. 按 `F5` 選擇 "Python: Train YOLO Model"
4. 除錯開始

**中斷點位置建議**:
- 模型載入後
- 訓練開始前
- 每個 epoch 結束

---

### 除錯 API

1. 開啟 `src/api/main.py`
2. 設定中斷點在端點函數內
3. 按 `F5` 選擇 "Python: FastAPI Debug"
4. API 啟動在 http://localhost:8000
5. 發送請求觸發中斷點

**測試方式**:
```bash
# 使用 curl
curl -X POST "http://localhost:8000/predict" \
  -F "file=@test.jpg"

# 或開啟 Swagger UI
# http://localhost:8000/docs
```

---

### 除錯測試

1. 開啟測試檔案
2. 設定中斷點
3. 按 `F5` 選擇 "Python: Pytest (Current File)"
4. 除錯該測試檔案

---

## 🎯 任務使用指南

### 執行任務的方式

#### 方法 1: 命令面板
```bash
Cmd+Shift+P (macOS) / Ctrl+Shift+P (Windows)
→ Tasks: Run Task
→ 選擇任務
```

#### 方法 2: 快捷鍵
```bash
Cmd+Shift+B (macOS) / Ctrl+Shift+B (Windows)
→ 執行預設建置任務 (Code Quality Check)
```

#### 方法 3: 終端選單
```
Terminal → Run Task → 選擇任務
```

---

### 常用任務組合

#### 提交前檢查
```
1. Code Quality Check (All)  # Cmd+Shift+B
2. Run Tests (pytest)
3. Git: Commit with Claude
```

#### 訓練前準備
```
1. Validate Dataset
2. Download YOLO Models (if needed)
3. Train YOLO Model
```

#### API 開發流程
```
1. Start FastAPI Server
2. Open Swagger UI
3. (使用 REST Client 測試)
4. (除錯如需要)
```

---

## 💡 程式碼片段使用指南

### 基本使用

1. 輸入片段前綴
2. 按 `Tab` 展開
3. 使用 `Tab` 在佔位符間跳轉
4. 按 `Esc` 退出片段模式

---

### 常用片段範例

#### 建立訓練腳本
```python
yolo-train<Tab>

# 展開為完整的訓練腳本
# 自動跳到參數位置讓你填寫
```

#### 建立 API 端點
```python
fastapi-yolo-predict<Tab>

# 展開為完整的預測端點
# 包含圖片上傳、預測、結果格式化
```

#### 建立測試
```python
pytest-test<Tab>

# 展開為 AAA 模式測試
# (Arrange, Act, Assert)
```

---

### 自訂片段

編輯 `yolo.code-snippets` 新增自己的片段:

```json
{
  "My Custom Snippet": {
    "prefix": "my-snippet",
    "body": [
      "def ${1:function_name}():",
      "    ${2:pass}",
      "$0"
    ],
    "description": "My custom code snippet"
  }
}
```

---

## ⌨️ 鍵盤快捷鍵

### 預設快捷鍵

| 功能 | macOS | Windows/Linux |
|------|-------|---------------|
| 執行建置任務 | `Cmd+Shift+B` | `Ctrl+Shift+B` |
| 開始除錯 | `F5` | `F5` |
| 停止除錯 | `Shift+F5` | `Shift+F5` |
| 繼續執行 | `F5` | `F5` |
| 單步執行 | `F10` | `F10` |
| 進入函數 | `F11` | `F11` |
| 跳出函數 | `Shift+F11` | `Shift+F11` |
| 切換中斷點 | `F9` | `F9` |
| 命令面板 | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| 快速開啟 | `Cmd+P` | `Ctrl+P` |
| 終端 | `` Ctrl+` `` | `` Ctrl+` `` |
| 問題面板 | `Cmd+Shift+M` | `Ctrl+Shift+M` |
| 測試瀏覽器 | `Cmd+Shift+T` | `Ctrl+Shift+T` |

---

### 自訂快捷鍵

編輯 `keybindings.json`:

```bash
Cmd+Shift+P → Preferences: Open Keyboard Shortcuts (JSON)
```

範例:
```json
[
  {
    "key": "cmd+shift+r",
    "command": "workbench.action.tasks.runTask",
    "args": "Run Tests (pytest)"
  },
  {
    "key": "cmd+shift+v",
    "command": "workbench.action.tasks.runTask",
    "args": "Validate Dataset"
  }
]
```

---

## ❓ 常見問題

### Q: 擴展無法安裝？

**A**: 檢查網路連線或手動安裝:
```bash
code --install-extension ms-python.python
```

---

### Q: Python 解釋器找不到？

**A**: 手動設定:
```bash
Cmd+Shift+P → Python: Select Interpreter
→ 選擇正確的 Python 路徑
```

---

### Q: Black 格式化不工作？

**A**: 檢查:
1. Black 是否安裝: `pip install black`
2. 擴展是否啟用: `ms-python.black-formatter`
3. 設定是否正確: `"editor.formatOnSave": true`

---

### Q: 除錯無法啟動？

**A**: 檢查:
1. `launch.json` 路徑是否正確
2. Python 解釋器是否選擇
3. 依賴是否安裝

---

### Q: 任務執行失敗？

**A**: 檢查:
1. 命令是否存在 (`which black`, `which pytest`)
2. 檔案路徑是否正確
3. 終端輸出的錯誤訊息

---

### Q: 程式碼片段不展開？

**A**: 確認:
1. 語言模式正確 (Python)
2. 輸入完整前綴
3. 按 `Tab` 鍵而非 `Enter`

---

### Q: Git 擴展顯示太多？

**A**: 可在設定中調整:
```json
{
  "gitlens.codeLens.enabled": false,
  "gitlens.hovers.enabled": false
}
```

---

## 📚 相關資源

### VS Code 官方文檔
- [Python in VS Code](https://code.visualstudio.com/docs/languages/python)
- [Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [Tasks](https://code.visualstudio.com/docs/editor/tasks)
- [Snippets](https://code.visualstudio.com/docs/editor/userdefinedsnippets)

### 專案文檔
- [README.md](../README.md) - 專案總覽
- [CLAUDE.md](../CLAUDE.md) - 開發規範
- [.devcontainer/README.md](../.devcontainer/README.md) - Dev Container 文檔
- [scripts/README.md](../scripts/README.md) - 腳本工具

---

## 🎉 總結

VS Code 配置已完成！現在你可以:

✅ **一鍵安裝推薦擴展**
✅ **自動格式化和 linting**
✅ **強大的除錯功能**
✅ **快速執行任務**
✅ **使用程式碼片段加速開發**

**下一步**:
1. 安裝推薦擴展
2. 選擇 Python 解釋器
3. 執行 "Code Quality Check" 任務測試設定
4. 試試程式碼片段 (`yolo-train<Tab>`)
5. 開始開發！

祝開發順利！🚀
