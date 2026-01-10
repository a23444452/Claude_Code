# GitHub 整合工具

本目錄包含 GitHub 專案管理和自動化工具，協助維護程式碼品質、處理 issues、自動化測試等。

## 📋 目錄結構

```
.github/
├── ISSUE_TEMPLATE/          # Issue 模板
│   ├── config.yml           # Issue 模板配置
│   ├── bug_report.yml       # Bug 回報模板
│   ├── training_issue.yml   # 訓練問題模板
│   ├── api_issue.yml        # API 問題模板
│   ├── feature_request.yml  # 功能請求模板
│   └── documentation.yml    # 文檔問題模板
├── workflows/               # GitHub Actions 工作流程
│   ├── code-quality.yml     # 程式碼品質檢查
│   ├── validate-commit.yml  # 提交內容驗證
│   ├── security-scan.yml    # 安全性掃描
│   ├── test.yml            # 自動化測試
│   ├── docs-validation.yml  # 文檔驗證
│   ├── stale-issue-manager.yml  # 過期 Issue 管理
│   └── model-validation.yml # 模型驗證
├── prompts/                 # Claude Code 提示模板
│   ├── training-assistant.prompt.md    # 訓練助手
│   ├── api-debugger.prompt.md         # API 除錯
│   ├── dataset-analyzer.prompt.md     # 資料集分析
│   └── model-optimizer.prompt.md      # 模型優化
├── pull_request_template.md # PR 模板
└── README.md               # 本文件
```

---

## 📝 Issue 模板

### 使用方式
當建立新 Issue 時，GitHub 會自動提供以下模板選擇：

### 1. 🐛 Bug 回報 (`bug_report.yml`)
用於回報程式錯誤、異常行為等問題。

**包含內容:**
- 問題類型（訓練/推論/API/資料處理）
- 重現步驟
- 預期行為 vs 實際行為
- 環境資訊（Python、套件版本、作業系統）
- 錯誤日誌和截圖

### 2. 🎯 訓練問題 (`training_issue.yml`)
專門處理模型訓練相關的問題。

**包含內容:**
- 問題類型（訓練停滯、過擬合、記憶體不足等）
- 資料集資訊
- 訓練配置和日誌
- 當前指標（mAP, Loss, Precision, Recall）
- 硬體資訊

### 3. 🔌 API 問題 (`api_issue.yml`)
回報 FastAPI 後端相關的問題。

**包含內容:**
- 問題類型（端點錯誤、效能問題、CORS 等）
- 相關端點
- 請求/回應範例
- API 日誌
- 效能資訊

### 4. ✨ 功能請求 (`feature_request.yml`)
建議新功能或改進。

**包含內容:**
- 功能類別
- 問題或需求描述
- 提議的解決方案
- 使用場景和預期效益
- 優先級評估

### 5. 📚 文檔問題 (`documentation.yml`)
回報文檔錯誤或建議改進。

**包含內容:**
- 文檔類型（README、API 文檔、註解等）
- 問題類型（內容錯誤、資訊過時、連結失效等）
- 當前內容和建議內容

---

## 🔄 GitHub Actions 工作流程

### 1. 🔍 程式碼品質檢查 (`code-quality.yml`)

**觸發時機:**
- Pull Request 到 main/develop 分支
- Push 到 main/develop 分支

**檢查項目:**
- Black 程式碼格式化
- isort 匯入排序
- flake8 語法檢查
- mypy 型別檢查

**使用方式:**
```bash
# 本地執行檢查
black --check src/
isort --check-only src/
flake8 src/
mypy src/
```

### 2. 🚫 提交內容驗證 (`validate-commit.yml`)

**觸發時機:**
- Pull Request 到 main/develop 分支

**檢查項目:**
- ✅ 防止提交 `.pt` 模型檔案
- ✅ 防止提交資料集圖片/標註
- ✅ 防止提交敏感配置檔案
- ✅ 檢查大檔案（>10MB）
- ✅ 檢查敏感資訊（.env, keys）
- ✅ 驗證 Conventional Commits 格式

**重要性:** 🔴 最重要的工作流程之一，防止意外提交大檔案到 Git。

### 3. 🔒 安全性掃描 (`security-scan.yml`)

**觸發時機:**
- Pull Request
- Push 到 main 分支
- 每週一自動執行

**檢查項目:**
- Bandit 安全性漏洞掃描
- 依賴套件漏洞檢查（pip-audit）
- 硬編碼密鑰檢測
- 常見安全問題（eval, exec, pickle, shell=True）

**報告:** 掃描報告會上傳為 artifact，可下載查看。

### 4. 🧪 自動化測試 (`test.yml`)

**觸發時機:**
- Pull Request
- Push 到 main/develop 分支

**測試環境:**
- Ubuntu + macOS
- Python 3.10 + 3.11

**功能:**
- 執行 pytest 單元測試
- 產生覆蓋率報告
- 上傳至 Codecov

### 5. 📚 文檔驗證 (`docs-validation.yml`)

**觸發時機:**
- Pull Request

**檢查項目:**
- 程式碼變更是否需要更新 README
- README 內部連結是否失效
- 必要章節是否完整
- CLAUDE.md 是否存在
- Plugin 和 Command 文檔完整性

**用途:** 確保文檔與程式碼保持同步。

### 6. 🗂️ 過期 Issue 管理 (`stale-issue-manager.yml`)

**觸發時機:**
- 每日 00:00 UTC 自動執行
- 可手動觸發

**行為:**
- Issue 30 天無活動 → 標記為 stale
- PR 14 天無活動 → 標記為 stale
- Stale 後 7 天仍無活動 → 自動關閉

**豁免:** 包含 `pinned`, `security`, `bug`, `enhancement` 等標籤的 issue 不會被自動關閉。

### 7. 🎯 模型驗證 (`model-validation.yml`)

**觸發時機:**
- 手動觸發（workflow_dispatch）
- Release 發布時

**功能:**
- 驗證模型檔案完整性
- 測試模型推論功能
- 產生模型資訊報告

**使用方式:**
```bash
# 在 GitHub Actions 頁面手動觸發
# 可指定模型路徑和測試圖片數量
```

---

## 💡 提示模板 (Prompts)

提示模板協助你更有效地使用 Claude Code 解決問題。

### 1. 🎯 訓練助手 (`training-assistant.prompt.md`)

**用途:** 診斷和解決訓練問題（過擬合、欠擬合、訓練停滯等）

**使用時機:**
- Loss 不下降
- 驗證集表現遠差於訓練集
- mAP 一直很低
- 訓練速度異常

**使用方式:**
1. 複製模板內容
2. 填寫訓練配置、當前指標、問題描述
3. 貼上訓練日誌
4. 讓 Claude 分析並提供解決方案

**配合工具:**
- `/dataset-analyzer` - 檢查資料集品質
- `/model-optimizer` - 獲得優化建議

### 2. 🔌 API 除錯助手 (`api-debugger.prompt.md`)

**用途:** 診斷和解決 FastAPI 後端問題

**使用時機:**
- API 無法啟動
- 端點回應錯誤
- 效能問題（回應慢）
- CORS 或認證問題

**使用方式:**
1. 複製模板內容
2. 提供環境資訊、錯誤訊息
3. 貼上請求/回應範例和 API 日誌
4. 讓 Claude 診斷並提供修正

**配合工具:**
- `/api-test` - 測試 API 端點
- `/api-security` - 安全性檢查

### 3. 📊 資料集分析助手 (`dataset-analyzer.prompt.md`)

**用途:** 分析資料集品質、發現問題、提供改進建議

**使用時機:**
- 訓練效果不佳
- 某些類別辨識率低
- 不確定標註品質
- 類別分布不平衡

**使用方式:**
1. 執行 `/dataset-analyzer --dataset [路徑]`
2. 複製模板，填寫資料集資訊
3. 貼上分析報告
4. 讓 Claude 解讀並提供改進建議

**常見問題:**
- 類別不平衡 → 過採樣/資料增強
- 標註品質差 → 重新審查標註
- 圖片品質差 → 過濾或改善拍攝

### 4. ⚡ 模型優化助手 (`model-optimizer.prompt.md`)

**用途:** 分析模型效能、提供優化建議（速度、記憶體、準確度）

**使用時機:**
- 需要部署到邊緣裝置
- 推論速度太慢
- 記憶體使用過高
- 準確度需要提升

**使用方式:**
1. 執行 `/model-optimizer --model [路徑] --analyze`
2. 複製模板，填寫模型資訊和效能指標
3. 明確說明優化目標
4. 讓 Claude 提供優化策略

**優化技術:**
- 模型量化（INT8/FP16）
- 選擇合適的模型大小（n/s/m/l/x）
- TensorRT/ONNX 優化
- 批次推論

---

## 📋 Pull Request 模板

### 使用方式
建立 PR 時會自動套用此模板。

### 包含章節

#### 1. 變更說明
- 簡要描述 PR 目的和變更內容
- 勾選變更類型（Bug 修復、新功能、文檔更新等）

#### 2. 相關 Issue
- 連結相關的 issue

#### 3. 變更細節
- 主要變更項目
- 技術實作細節
- 破壞性變更說明

#### 4. 測試
- 測試方式（單元測試、整合測試、手動測試）
- 測試步驟
- 測試結果

#### 5. 文檔更新
- 確認是否更新相關文檔

#### 6. 檢查清單
- **程式碼品質**: PEP8、Type Hints、docstring
- **Git 規範**: Commit message、無模型檔案、無敏感資訊
- **安全性**: 執行 `/api-security` 檢查
- **效能**: 考慮效能影響
- **相容性**: 向後相容性

---

## 🚀 最佳實踐

### 建立 Issue 時
1. ✅ 選擇正確的 Issue 模板
2. ✅ 完整填寫所有必填欄位
3. ✅ 提供足夠的重現步驟或範例
4. ✅ 貼上相關的錯誤日誌或截圖
5. ✅ 標註適當的 labels

### 建立 Pull Request 時
1. ✅ 確保通過所有 CI 檢查
2. ✅ 完整填寫 PR 模板
3. ✅ 自我 review 程式碼
4. ✅ 確認沒有提交模型檔案或資料集
5. ✅ 更新相關文檔
6. ✅ 撰寫或更新測試

### Commit Message 規範
遵循 **Conventional Commits** 格式：

```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Type 類型:**
- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文檔更新
- `style`: 格式調整（不影響程式碼邏輯）
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 雜項（依賴更新、配置變更）
- `perf`: 效能優化
- `ci`: CI/CD 變更

**範例:**
```
feat(api): add batch prediction endpoint

Add new /predict/batch endpoint to support multiple image predictions.
- Accept multiple file uploads
- Process images in parallel
- Return combined results

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 使用提示模板
1. ✅ 先執行相關的 Claude Code 命令（如 `/dataset-analyzer`）
2. ✅ 完整填寫模板中的所有資訊
3. ✅ 提供具體的數據和日誌
4. ✅ 明確說明目標和限制
5. ✅ 根據建議迭代改進

---

## 🔧 設定和自訂

### 啟用 GitHub Actions
1. 確保專案已推送到 GitHub
2. Actions 會自動在 PR 和 Push 時觸發
3. 可在 Settings > Actions 調整權限

### 自訂 Workflow
編輯 `.github/workflows/*.yml` 檔案以調整行為。

**常見調整:**
- 修改觸發條件（分支、路徑）
- 調整檢查嚴格程度
- 新增或移除檢查項目
- 修改通知設定

### 自訂 Issue 模板
編輯 `.github/ISSUE_TEMPLATE/*.yml` 檔案。

**可調整項目:**
- 新增或移除欄位
- 修改選項內容
- 調整驗證規則
- 更新說明文字

---

## 📚 相關資源

### 內部文檔
- [CLAUDE.md](../CLAUDE.md) - 專案開發規範
- [README.md](../README.md) - 專案總覽
- [ARCHITECTURE.md](../ARCHITECTURE.md) - 系統架構（如有）
- [USAGE.md](../USAGE.md) - 使用指南（如有）

### GitHub 功能
- [GitHub Actions 文檔](https://docs.github.com/en/actions)
- [Issue 模板文檔](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
- [Conventional Commits](https://www.conventionalcommits.org/)

### Claude Code
- [Commands](./.claude/commands/) - 可用命令
- [Plugins](./.claude/plugins/) - 可用插件
- [Hooks](./.claude/hooks/) - 驗證鉤子

---

## 🤝 貢獻

歡迎改進這些工具！

### 如何貢獻
1. Fork 此專案
2. 建立功能分支
3. 提交你的變更
4. 建立 Pull Request

### 建議改進方向
- 新增更多 Issue 模板
- 改進 Workflow 檢查
- 新增更多提示模板
- 優化自動化流程
- 改進文檔

---

## 📞 支援

如有問題或建議：

1. **使用 Issue 模板** 建立對應的 issue
2. **使用提示模板** 尋求 Claude Code 協助
3. **查看文檔** [CLAUDE.md](../CLAUDE.md) 了解開發規範
4. **檢查 Workflows** 查看 CI/CD 執行結果

---

**感謝使用這些工具！** 🎉

這些自動化工具和模板旨在提升開發效率、維護程式碼品質，並促進團隊協作。
