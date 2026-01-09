# YOLO Project Plugins

專為 YOLO 物件偵測專案設計的 Claude Code 插件集合。

## 插件列表

### 📊 [Dataset Analyzer](dataset-analyzer/)
資料集深度分析工具

**功能：**
- 統計分析（類別分布、尺寸分布）
- 品質檢查（遺失檔案、格式錯誤）
- 視覺化分析（分布圖表、熱圖）
- 問題偵測（不平衡、異常標註）

**使用：**
```bash
/dataset-analyzer
/dataset-analyzer --path dataset/my_dataset --visualize
```

**適用場景：**
- 訓練前資料品質檢查
- 新增資料後的驗證
- 資料集不平衡診斷
- 標註品質審查

---

### ⚡ [Model Optimizer](model-optimizer/)
模型優化建議工具

**功能：**
- 效能分析（推論速度、記憶體使用）
- 訓練分析（過擬合檢測、收斂評估）
- 優化建議（架構選擇、超參數調整）
- 量化評估（FP16/INT8 建議）

**使用：**
```bash
/model-optimizer
/model-optimizer --weights best.pt --benchmark
```

**適用場景：**
- 訓練完成後的效能評估
- 模型選擇和比較
- 部署前的優化建議
- 速度/精度權衡分析

---

### 🔒 [API Security](api-security/)
API 安全性檢查工具

**功能：**
- OWASP Top 10 漏洞掃描
- 程式碼安全審查（注入攻擊、XSS）
- 配置審查（CORS、認證、Rate Limiting）
- 依賴漏洞檢測

**使用：**
```bash
/api-security
/api-security --detailed
```

**適用場景：**
- API 開發後的安全檢查
- 部署前的漏洞掃描
- 定期安全審計
- Code review 輔助

---

### 📈 [Training Monitor](training-monitor/)
訓練即時監控工具

**功能：**
- 即時監控（進度、Loss、指標）
- 異常偵測（Loss 爆炸、過擬合）
- 效能分析（訓練速度、資源使用）
- 智慧通知（完成提醒、異常警告）

**使用：**
```bash
/training-monitor --watch
/training-monitor --report
```

**適用場景：**
- 長時間訓練監控
- 訓練異常偵測
- 多實驗比較
- 遠端訓練追蹤

---

## 快速開始

### 安裝
插件已包含在專案中，無需額外安裝。確保你使用的是最新版本的 Claude Code。

### 基本使用
在專案根目錄下直接使用命令：
```bash
# 資料集分析
/dataset-analyzer

# 模型優化
/model-optimizer

# 安全檢查
/api-security

# 訓練監控
/training-monitor --watch
```

### 完整工作流程
```bash
# 1. 資料準備
/preprocess
/dataset-analyzer              # 檢查資料品質

# 2. 模型訓練
/train --epochs 100 &
/training-monitor --watch      # 即時監控訓練

# 3. 模型優化
/model-optimizer --benchmark   # 分析效能並獲取建議

# 4. API 部署
/start-services
/api-security                  # 安全檢查
/api-test                      # 功能測試

# 5. 驗證和發布
/validate
/commit-push
```

## 插件架構

每個插件包含以下結構：
```
plugin-name/
├── .claude-plugin/
│   └── config.json      # 插件配置
├── README.md            # 詳細文檔
└── commands/            # 命令實作（可選）
```

### 配置檔案結構
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "插件描述",
  "commands": [...],
  "thresholds": {...},
  "checks": {...}
}
```

## 自定義配置

每個插件都支援自定義配置，編輯對應的 `config.json` 檔案：

### Dataset Analyzer 配置
```json
{
  "thresholds": {
    "class_imbalance_ratio": 3.0,
    "min_bbox_size": 10
  }
}
```

### Model Optimizer 配置
```json
{
  "thresholds": {
    "good_map": 0.7,
    "excellent_map": 0.9
  }
}
```

### API Security 配置
```json
{
  "severity_levels": {
    "critical": ["authentication", "injection"],
    "high": ["rate_limiting", "cors"]
  }
}
```

### Training Monitor 配置
```json
{
  "watch_mode": {
    "update_interval": 10
  },
  "alerts": {
    "loss_spike_threshold": 0.5
  }
}
```

## 插件輸出

所有插件的輸出檔案統一儲存在對應目錄：

```
project-root/
├── analysis/              # Dataset Analyzer 輸出
│   ├── dataset_report.txt
│   └── *.png
├── monitoring/            # Training Monitor 輸出
│   ├── training_log.txt
│   └── *.png
├── optimization/          # Model Optimizer 輸出
│   ├── model_report.txt
│   └── benchmark_results.json
└── security/              # API Security 輸出
    ├── scan_report.txt
    └── vulnerabilities.json
```

## 最佳實踐

### 開發階段
1. 使用 Dataset Analyzer 確保資料品質
2. 使用 Training Monitor 追蹤訓練過程
3. 使用 Model Optimizer 評估模型效能
4. 使用 API Security 檢查程式碼安全

### 部署前
1. 執行完整的安全掃描（評分 > 80）
2. 確認模型效能符合要求
3. 驗證資料集品質
4. 檢查所有測試通過

### 生產環境
1. 定期執行安全掃描
2. 監控模型效能退化
3. 追蹤資料分布變化
4. 記錄訓練歷史

## 整合建議

### 與 Commands 配合
```bash
# 資料處理流程
/preprocess → /dataset-analyzer → /train

# 訓練流程
/train → /training-monitor → /validate

# 部署流程
/model-optimizer → /api-security → /start-services

# 完整流程
/project-status  # 查看整體狀態
```

### CI/CD 整合
```yaml
# .github/workflows/ci.yml
- name: Check Dataset
  run: claude /dataset-analyzer

- name: Train Model
  run: python src/training/train.py

- name: Monitor Training
  run: claude /training-monitor --report

- name: Optimize Model
  run: claude /model-optimizer

- name: Security Scan
  run: claude /api-security
```

## 故障排除

### 插件無法執行
- 確認 Claude Code 版本
- 檢查配置檔案格式
- 查看錯誤日誌

### 輸出不完整
- 確認檔案權限
- 檢查磁碟空間
- 驗證輸入路徑

### 效能問題
- 減少分析範圍
- 調整更新頻率
- 優化配置參數

## 貢獻

歡迎提交新的插件或改進現有插件！

### 開發新插件
1. 在 `.claude/plugins/` 下創建新目錄
2. 添加 `.claude-plugin/config.json` 配置
3. 撰寫 `README.md` 文檔
4. 測試功能完整性
5. 提交 Pull Request

### 改進現有插件
1. Fork 專案
2. 修改對應插件
3. 更新文檔
4. 提交 Pull Request

## 版本歷史

### v1.0.0 (2026-01-09)
- ✅ Dataset Analyzer - 資料集分析工具
- ✅ Model Optimizer - 模型優化建議
- ✅ API Security - 安全性檢查
- ✅ Training Monitor - 訓練監控

## 授權

本插件集合遵循專案的 MIT 授權條款。

## 聯絡

- GitHub: [a23444452/Claude_Code](https://github.com/a23444452/Claude_Code)
- Issues: [提交問題](https://github.com/a23444452/Claude_Code/issues)

---

<div align="center">

**讓 YOLO 開發更高效！**

[回到專案首頁](../../../README.md)

</div>
