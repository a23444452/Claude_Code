# YOLO Project Development Container

這個目錄包含 VS Code Dev Container 配置，提供一致的開發環境，適用於 YOLO 物件偵測專案開發。

## 📋 目錄

- [特色](#特色)
- [前置需求](#前置需求)
- [快速開始](#快速開始)
- [容器內容](#容器內容)
- [網路安全](#網路安全)
- [常見問題](#常見問題)
- [進階配置](#進階配置)
- [疑難排解](#疑難排解)

---

## ✨ 特色

### 🐍 Python 開發環境
- **Python 3.10** 預裝，針對 YOLO 開發優化
- **PyTorch** 和相關深度學習套件支援
- **Ultralytics YOLO** 開箱即用
- **FastAPI** 用於後端 API 開發

### 🛠️ 開發工具
- **Claude Code CLI** - AI 輔助編程工具
- **Git Delta** - 增強的 git diff 檢視
- **Zsh** with autosuggestions - 強大的 shell
- **Git LFS** - 大檔案版本控制
- **GitHub CLI** - GitHub 命令列工具

### 📦 程式碼品質工具
- **Black** - 自動程式碼格式化
- **isort** - 匯入排序
- **Flake8** - Linting
- **mypy** - 型別檢查
- **pytest** - 測試框架

### 🔒 安全性
- **防火牆隔離** - 限制網路存取僅允許必要服務
- **非 root 使用者** - 以 `yolo` 使用者身份執行
- **最小權限原則** - 僅授予必要權限

### 🔌 VS Code 整合
- 預裝 20+ 實用擴展
- Python、Git、Docker、Jupyter 完整支援
- 自動格式化和 linting
- 整合除錯工具

---

## 📋 前置需求

### 必要軟體
1. **Docker Desktop**
   - [下載 Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - 確保 Docker 正在運行

2. **Visual Studio Code**
   - [下載 VS Code](https://code.visualstudio.com/)
   - 安裝 [Dev Containers 擴展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### 系統需求
- **記憶體**: 至少 8GB RAM（建議 16GB）
- **磁碟空間**: 至少 10GB 可用空間
- **作業系統**: Windows 10/11, macOS 10.15+, 或 Linux

### 可選但建議
- **GPU 支援** (NVIDIA CUDA 或 Apple Silicon)
- **快速網路連線** (首次建置時下載大量套件)

---

## 🚀 快速開始

### 方法 1: 使用 VS Code 命令面板（推薦）

1. **開啟專案**
   ```bash
   cd /path/to/YOLO_Project
   code .
   ```

2. **開啟 Dev Container**
   - 按 `F1` 或 `Cmd/Ctrl+Shift+P` 開啟命令面板
   - 輸入並選擇：`Dev Containers: Reopen in Container`
   - 等待容器建置（首次約 5-10 分鐘）

3. **開始開發**
   - 容器啟動後，你將在完整配置的開發環境中
   - 開啟終端機（`` Ctrl+` ``），預設為 zsh

### 方法 2: 使用提示通知

1. 開啟專案資料夾
2. VS Code 會偵測到 `.devcontainer` 配置
3. 點擊右下角的提示「Reopen in Container」

### 方法 3: 從命令列

```bash
# Clone 專案
git clone https://github.com/a23444452/Claude_Code.git YOLO_Project
cd YOLO_Project

# 使用 Dev Container CLI
devcontainer open .
```

---

## 📦 容器內容

### 已安裝的工具

#### 系統工具
```
git, git-lfs, curl, wget, vim, nano, zsh
iptables, ipset, dnsutils
build-essential, python3-dev
```

#### Python 開發
```
Python 3.10
pip, setuptools, wheel
black, isort, flake8, mypy, pylint
pytest, pytest-cov, pytest-asyncio
```

#### 影像處理
```
OpenCV dependencies
libgl1-mesa-glx, libglib2.0-0
```

#### Node.js (for Claude Code)
```
Node.js 20
npm
@anthropic-ai/claude-code
```

#### Git 增強
```
git-delta (better diffs)
GitHub CLI (gh)
Git LFS
```

### VS Code 擴展

#### Python 開發
- Python
- Pylance
- Black Formatter
- isort
- Flake8
- mypy

#### Git
- GitLens
- Git History
- Git Graph

#### 其他
- Claude Code
- YAML Support
- Markdown All in One
- Docker
- REST Client
- Error Lens
- Jupyter
- Better Comments

### 連接埠轉發

容器自動轉發以下連接埠：

| 連接埠 | 服務 | 用途 |
|-------|------|------|
| 8000 | FastAPI | 後端 API 伺服器 |
| 8888 | Jupyter | Jupyter Notebook |

### 持久化儲存

以下目錄使用 Docker volumes 持久化：

- `/commandhistory` - Bash/Zsh 歷史記錄
- `/home/yolo/.claude` - Claude Code 配置
- `/home/yolo/.cache/pip` - pip 快取

**好處**: 即使重建容器，這些資料也會保留。

---

## 🔒 網路安全

### 防火牆配置

容器啟動時會執行 `init-firewall.sh`，配置嚴格的防火牆規則。

#### ✅ 允許的服務

**開發必要服務:**
- 🐙 **GitHub** - 程式碼託管
- 🐍 **PyPI** - Python 套件
- 🔥 **PyTorch** - 深度學習框架
- 📦 **npm** - Node.js 套件
- 🤖 **Anthropic API** - Claude Code
- 💻 **VSCode** - 編輯器服務
- 🎯 **Ultralytics** - YOLO 資源
- 🐳 **Docker Hub** - 容器映像

**基礎服務:**
- 🏠 **localhost** - 本機通訊
- 🔍 **DNS** (port 53) - 域名解析
- 🔐 **SSH** (port 22) - 安全連線

#### ❌ 封鎖的服務

**預設政策**: 所有其他網路流量被封鎖

**範例:**
- ❌ example.com
- ❌ 任意第三方 API
- ❌ 未經授權的網站

### 為什麼需要防火牆？

1. **安全性** - 防止未經授權的網路存取
2. **資料保護** - 限制資料外流
3. **合規性** - 符合企業安全政策
4. **專注開發** - 僅允許開發相關服務

### 自訂防火牆規則

如需允許額外的域名，編輯 `init-firewall.sh`:

```bash
# Add custom domain
echo "🌐 Resolving custom domain..."
resolve_and_add "your-custom-domain.com"
```

---

## ❓ 常見問題

### Q: 首次建置需要多久？

**A**: 約 5-10 分鐘，取決於網路速度。後續啟動僅需 10-30 秒。

### Q: 容器重啟後我的檔案會消失嗎？

**A**: 不會。`/workspace` 映射到本機專案目錄，所有變更都會保存。

### Q: 如何在容器內安裝 Python 套件？

**A**: 使用 pip，套件會安裝到使用者目錄：
```bash
pip install --user package-name
```

如需持久化，將套件加到 `requirements.txt`。

### Q: 可以使用 GPU 嗎？

**A**: 可以！需要額外配置：

**NVIDIA GPU:**
1. 安裝 [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)
2. 修改 `devcontainer.json`：
```json
"runArgs": [
  "--gpus=all"
]
```

**Apple Silicon (M1/M2):**
- 預設支援 MPS (Metal Performance Shaders)
- PyTorch 會自動使用 MPS 加速

### Q: 如何在容器內執行 Claude Code 命令？

**A**: 開啟終端機，直接執行：
```bash
/train
/api-test
/dataset-analyzer --dataset dataset/your_dataset
```

### Q: 防火牆太嚴格，某些網站無法存取？

**A**: 編輯 `init-firewall.sh` 新增域名，或暫時停用防火牆：
```bash
sudo iptables -P OUTPUT ACCEPT
```

⚠️ **注意**: 停用防火牆會降低安全性。

### Q: 如何更新容器？

**A**: 重建容器以獲取最新配置：
1. `F1` → `Dev Containers: Rebuild Container`
2. 或使用 Docker CLI: `docker-compose build --no-cache`

### Q: 容器佔用多少磁碟空間？

**A**:
- 基礎映像: ~2GB
- 已安裝套件: ~3GB
- 總計: ~5GB

### Q: 可以在容器內使用 Docker 嗎？

**A**: 可以（Docker-in-Docker），但需要修改配置。通常不建議，使用 `--network=host` 已足夠。

---

## ⚙️ 進階配置

### 修改 Python 版本

編輯 `Dockerfile`:
```dockerfile
FROM python:3.11-slim  # 改為 3.11
```

### 修改時區

編輯 `devcontainer.json`:
```json
"args": {
  "TIMEZONE": "America/New_York"
}
```

### 新增 VS Code 擴展

編輯 `devcontainer.json`:
```json
"extensions": [
  "existing.extensions",
  "your-new.extension"
]
```

### 自訂環境變數

編輯 `devcontainer.json`:
```json
"containerEnv": {
  "YOUR_VAR": "value"
}
```

### 修改連接埠轉發

編輯 `devcontainer.json`:
```json
"forwardPorts": [8000, 8888, 5000],
"portsAttributes": {
  "5000": {
    "label": "Custom Service"
  }
}
```

### 使用 Docker Compose

如需更複雜的設定（如資料庫），可建立 `docker-compose.yml`:

```yaml
version: '3.8'
services:
  yolo-dev:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example
```

然後修改 `devcontainer.json`:
```json
"dockerComposeFile": "docker-compose.yml",
"service": "yolo-dev",
"workspaceFolder": "/workspace"
```

---

## 🔧 疑難排解

### 問題: 容器無法啟動

**可能原因:**
- Docker 未運行
- 磁碟空間不足
- 記憶體不足

**解決方法:**
1. 確認 Docker Desktop 正在運行
2. 清理未使用的映像: `docker system prune -a`
3. 增加 Docker 記憶體限制（Docker Desktop → Settings → Resources）

### 問題: 建置過程卡住

**可能原因:**
- 網路連線問題
- 防火牆規則太嚴格

**解決方法:**
1. 檢查網路連線
2. 暫時註解 `postStartCommand` 中的防火牆初始化
3. 重新建置容器

### 問題: pip install 失敗

**可能原因:**
- 防火牆封鎖 PyPI
- 套件不相容

**解決方法:**
1. 檢查防火牆日誌
2. 確認 `init-firewall.sh` 已正確允許 PyPI
3. 使用 `--user` flag: `pip install --user package`

### 問題: Claude Code 命令找不到

**可能原因:**
- Node.js 未正確安裝
- PATH 環境變數問題

**解決方法:**
1. 檢查 Node.js: `node --version`
2. 重新安裝 Claude Code: `npm install -g @anthropic-ai/claude-code`
3. 確認 PATH: `echo $PATH`

### 問題: VS Code 擴展未自動安裝

**可能原因:**
- 網路問題
- Marketplace 無法存取

**解決方法:**
1. 手動安裝擴展
2. 檢查 `init-firewall.sh` 是否允許 `marketplace.visualstudio.com`
3. 重建容器: `Dev Containers: Rebuild Container`

### 問題: 效能很慢

**可能原因:**
- 檔案系統 I/O 瓶頸
- 記憶體不足

**解決方法:**
1. 使用 named volumes 而非 bind mounts
2. 增加 Docker 記憶體分配
3. 在 macOS 使用 `delegated` consistency:
```json
"mounts": [
  "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=delegated"
]
```

### 取得協助

如遇到問題:
1. 查看 Docker 日誌: `docker logs <container-id>`
2. 查看 VS Code Dev Container 日誌: `F1` → `Dev Containers: Show Container Log`
3. 在 [GitHub Issues](https://github.com/a23444452/Claude_Code/issues) 回報問題

---

## 📚 相關資源

### 官方文檔
- [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker Documentation](https://docs.docker.com/)
- [Dev Container Specification](https://containers.dev/)

### 專案文檔
- [CLAUDE.md](../CLAUDE.md) - 專案開發規範
- [README.md](../README.md) - 專案總覽
- [.github/README.md](../.github/README.md) - GitHub 工具

### 工具文檔
- [Claude Code](https://github.com/anthropics/claude-code)
- [Ultralytics YOLO](https://docs.ultralytics.com/)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## 🤝 貢獻

歡迎改進 Dev Container 配置！

**建議改進:**
- 新增更多實用工具
- 優化建置速度
- 改進防火牆規則
- 新增 GPU 支援範例
- 改善文檔

請提交 Pull Request 或建立 Issue。

---

## 📄 授權

此 Dev Container 配置遵循專案授權條款。

---

**享受一致且高效的開發體驗！** 🎉

如有任何問題或建議，歡迎在 [GitHub Issues](https://github.com/a23444452/Claude_Code/issues) 留言。
