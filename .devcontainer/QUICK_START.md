# 🚀 Dev Container 快速開始指南

5 分鐘快速上手 YOLO Project Dev Container！

## ⚡ 一鍵啟動

### 1. 確認前置條件
```bash
# 檢查 Docker 是否運行
docker --version

# 檢查 VS Code 是否安裝 Dev Containers 擴展
code --list-extensions | grep ms-vscode-remote.remote-containers
```

### 2. 開啟專案
```bash
cd YOLO_Project
code .
```

### 3. 啟動容器
按下 `F1`，輸入並選擇：
```
Dev Containers: Reopen in Container
```

### 4. 等待建置
⏱️ 首次建置約 5-10 分鐘，請耐心等待...

---

## ✅ 啟動後檢查清單

### 驗證環境
```bash
# 檢查 Python 版本
python --version  # 應顯示 Python 3.10.x

# 檢查 pip
pip --version

# 檢查 Claude Code
claude --version

# 檢查 git
git --version
```

### 測試工具
```bash
# 測試 Black 格式化
black --version

# 測試 pytest
pytest --version

# 測試 Claude Code 命令
/help
```

### 驗證網路
```bash
# 測試 PyPI 存取
pip search ultralytics || echo "PyPI accessible"

# 測試 GitHub 存取
git ls-remote https://github.com/ultralytics/ultralytics.git

# 測試防火牆（應該封鎖）
curl -s --max-time 2 http://example.com || echo "Firewall working!"
```

---

## 📦 安裝專案依賴

### 自動安裝（推薦）
容器啟動時會自動執行：
```bash
pip install --user -r requirements.txt
```

### 手動安裝
```bash
cd /workspace

# 安裝基礎依賴
pip install --user ultralytics fastapi uvicorn

# 或安裝完整依賴
pip install --user -r requirements.txt
```

---

## 🎯 常用命令

### Claude Code 命令
```bash
/train                    # 開始訓練
/api-test                # 測試 API
/dataset-analyzer        # 分析資料集
/model-optimizer         # 優化模型
/quick-predict           # 快速預測
/project-status          # 專案狀態
```

### Python 開發
```bash
# 格式化程式碼
black src/

# 排序 imports
isort src/

# Linting
flake8 src/

# 型別檢查
mypy src/

# 執行測試
pytest tests/
```

### Git 操作
```bash
git status
git add .
git commit -m "feat: your message"
git push

# 使用 Claude Code commit 助手
/commit-push
```

### API 開發
```bash
# 啟動 FastAPI 開發伺服器
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 或使用命令
/start-services
```

---

## 🔧 環境設定

### 配置環境變數
```bash
# 複製環境變數範例
cp .devcontainer/.env.example .env

# 編輯環境變數
nano .env
```

### 設定 API Key
```bash
# 在 .env 檔案中設定
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

---

## 🐛 快速除錯

### 容器無法啟動？
```bash
# 檢查 Docker 狀態
docker ps -a

# 查看容器日誌
docker logs <container_id>

# 重建容器
# F1 → Dev Containers: Rebuild Container
```

### Python 套件無法安裝？
```bash
# 檢查防火牆是否允許 PyPI
curl -s https://pypi.org

# 清除 pip 快取
pip cache purge

# 使用 --user flag
pip install --user package-name
```

### Claude Code 無法使用？
```bash
# 檢查 Node.js
node --version

# 重新安裝 Claude Code
npm install -g @anthropic-ai/claude-code

# 檢查 PATH
echo $PATH
```

---

## 📊 效能優化

### 首次建置優化
```bash
# 使用 BuildKit（更快）
export DOCKER_BUILDKIT=1

# 重建容器
docker-compose build --no-cache
```

### 運行時優化
```bash
# 增加 Docker 記憶體（Docker Desktop → Settings → Resources）
# 建議: 至少 8GB

# 使用 pip 快取
# 容器已自動配置 volume 快取
```

---

## 🎓 學習資源

### 容器內教學
```bash
# 查看完整文檔
cat .devcontainer/README.md

# 查看專案規範
cat CLAUDE.md

# 查看 API 文檔
cat README.md
```

### 線上資源
- [VS Code Dev Containers 文檔](https://code.visualstudio.com/docs/devcontainers/containers)
- [YOLO 專案 GitHub](https://github.com/a23444452/Claude_Code)
- [Ultralytics 文檔](https://docs.ultralytics.com/)

---

## 💡 實用技巧

### Tip 1: 使用 Zsh 自動補全
按 `Tab` 鍵啟用命令自動補全和建議。

### Tip 2: 快速導航
```bash
# 使用 fzf 快速搜尋檔案
Ctrl+T

# 搜尋命令歷史
Ctrl+R
```

### Tip 3: Git Delta 美化 diff
```bash
git diff  # 自動使用 delta 顯示
```

### Tip 4: VS Code 整合終端
`` Ctrl+` `` 快速開啟/關閉終端

### Tip 5: 多終端視窗
在終端右上角點擊 `+` 開啟新終端分頁。

---

## 🎉 開始開發！

環境已準備就緒，現在可以：

1. ✅ **瀏覽專案結構**
   ```bash
   tree -L 2 -I 'dataset|runs|__pycache__|*.pyc'
   ```

2. ✅ **查看範例程式碼**
   ```bash
   cat src/training/train.py  # 如果存在
   ```

3. ✅ **執行訓練**
   ```bash
   /train --help
   ```

4. ✅ **啟動 API**
   ```bash
   /start-services
   ```

5. ✅ **開啟 Swagger 文檔**
   在瀏覽器開啟: http://localhost:8000/docs

---

## 📞 需要協助？

### 查看文檔
```bash
cat .devcontainer/README.md  # 完整文檔
```

### GitHub Issues
[回報問題](https://github.com/a23444452/Claude_Code/issues)

### 使用 Claude Code
```bash
# 尋求協助
"請幫我解決 [問題描述]"

# 使用提示模板
cat .github/prompts/training-assistant.prompt.md
```

---

**祝開發順利！** 🚀

記得經常 commit 並 push 你的變更！
```bash
/commit-push
```
