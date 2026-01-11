# YOLO 物件偵測系統

<div align="center">

基於 **YOLO11n** 的即時物件偵測系統，提供完整的訓練、推論與 Web 介面。

[快速開始](#快速開始) • [功能特色](#功能特色) • [API 文檔](#api-文檔) • [架構說明](ARCHITECTURE.md) • [使用指南](USAGE.md)

</div>

---

## 專案簡介

這是一個完整的 YOLO 物件偵測解決方案，整合了：
- **資料處理**：自動化的圖片預處理與標註驗證
- **模型訓練**：支援 MPS 加速的 YOLO11n 訓練流程
- **後端 API**：基於 FastAPI 的高效能推論服務
- **前端介面**：直覺的 Web UI，支援拖曳上傳與即時結果顯示

適用於工業檢測、安全監控、品質控制等各種物件偵測場景。

---

## 功能特色

### 🚀 高效訓練
- 使用 **YOLO11n** 輕量級模型（2.59M 參數）
- 支援 **Apple Silicon MPS** 加速
- 內建資料增強與早停機制
- 訓練速度：~2秒/epoch

### 🎯 精準推論
- 單張圖片推論時間：~100-200ms
- 可調整信心度與 IOU 閾值
- 支援批次處理
- 自動 NMS（非極大值抑制）

### 🌐 RESTful API
- FastAPI 框架，自動生成文檔
- 多種端點：健康檢查、模型資訊、單張/批次偵測
- CORS 支援，易於整合
- 錯誤處理完善

### 💻 友善介面
- 現代化 Web UI
- 支援拖曳上傳與點擊上傳
- 即時結果視覺化（Canvas 繪圖）
- 參數即時調整

---

## 系統要求

### 基礎需求
- **Python**: 3.10 或以上
- **作業系統**: macOS、Linux 或 Windows
- **記憶體**: 建議 8GB 以上
- **儲存空間**: 至少 5GB（含資料集與模型）

### 加速支援
- **Apple Silicon** (M1/M2/M3): MPS 加速
- **NVIDIA GPU**: CUDA 加速
- **CPU**: 可運行但速度較慢

---

## 快速開始

### 1. 環境設定

建議使用 conda 或 venv 建立虛擬環境：

```bash
# 使用 conda（推薦）
conda create -n yolo_env python=3.10
conda activate yolo_env

# 或使用 venv
python3 -m venv yolo_env
source yolo_env/bin/activate  # macOS/Linux
# yolo_env\Scripts\activate  # Windows
```

### 2. 安裝依賴

```bash
# 安裝後端依賴
pip install -r src/api/requirements.txt

# 主要套件包括：
# - ultralytics (YOLO)
# - fastapi (API 框架)
# - uvicorn (ASGI 伺服器)
# - pillow (圖片處理)
# - torch (深度學習框架)
```

### 3. 啟動服務

#### 方式一：使用啟動腳本（推薦）
```bash
# 同時啟動後端和前端
./start_all.sh
```

#### 方式二：分別啟動
```bash
# 終端 1：啟動後端 API
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 終端 2：啟動前端
cd src/frontend && ./start_frontend.sh
```

### 4. 檢查服務狀態

使用服務檢查工具確認所有服務正常運行：

```bash
python3 check_services.py
```

輸出範例：
```
✅ API 服務: 運行中
   狀態: healthy
   模型已載入: True

✅ 前端服務: 運行中 (HTTP 200)

✅ 所有服務運行正常！

🌐 前端介面: http://localhost:3000
🔌 後端 API:  http://localhost:8000
📚 API 文檔:  http://localhost:8000/docs
```

### 5. 開始使用

1. 開啟瀏覽器訪問 **http://localhost:3000**
2. 上傳圖片（拖曳或點擊）
3. 調整偵測參數（選用）
4. 點擊「開始偵測」
5. 查看結果！

---

## 資料準備與訓練

### 準備資料集

將圖片與 YOLO 格式標註檔放入同一資料夾：

```
dataset/my_dataset/
├── image1.jpg
├── image1.txt  # YOLO 格式：class_id x_center y_center width height
├── image2.jpg
├── image2.txt
└── ...
```

### 資料預處理

```bash
python src/utils/preprocess.py \
  --source dataset/my_dataset \
  --output dataset/my_dataset_processed \
  --train-ratio 0.8
```

這會自動：
- ✅ 驗證圖片完整性
- ✅ 轉換為 RGB 格式
- ✅ 驗證標註正確性
- ✅ 隨機切分訓練/驗證集
- ✅ 生成類別清單

### 開始訓練

```bash
python src/training/train.py \
  --mode train \
  --data config/data.yaml \
  --epochs 100 \
  --batch 8 \
  --augment
```

**訓練參數說明：**
- `--mode`: `train` 訓練 | `validate` 驗證 | `test` 測試
- `--model`: 模型大小 `n`/`s`/`m`/`l`/`x`（預設：n）
- `--epochs`: 訓練輪數（預設：100）
- `--batch`: 批次大小（預設：8）
- `--imgsz`: 圖片尺寸（預設：640）
- `--augment`: 啟用資料增強

訓練完成後，模型儲存在 `runs/train/exp/weights/best.pt`

---

## API 文檔

### 端點總覽

| 端點 | 方法 | 功能 | 參數 |
|------|------|------|------|
| `/health` | GET | 健康檢查 | - |
| `/model/info` | GET | 模型資訊 | - |
| `/predict` | POST | 單張圖片偵測 | file, conf_threshold, iou_threshold |
| `/predict/batch` | POST | 批次圖片偵測 | files[] |

### 使用範例

#### Python
```python
import requests

with open('test.jpg', 'rb') as f:
    files = {'file': f}
    params = {
        'conf_threshold': 0.25,
        'iou_threshold': 0.45
    }
    response = requests.post(
        'http://localhost:8000/predict',
        files=files,
        params=params
    )
    result = response.json()

print(f"偵測到 {result['detection_count']} 個物件")
for det in result['detections']:
    print(f"{det['class_name']}: {det['confidence']:.2%}")
```

#### JavaScript
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/predict?conf_threshold=0.25', {
    method: 'POST',
    body: formData
});

const data = await response.json();
console.log(`偵測到 ${data.detection_count} 個物件`);
```

#### cURL
```bash
curl -X POST "http://localhost:8000/predict?conf_threshold=0.25" \
  -F "file=@test.jpg" | jq .
```

### 回應格式

```json
{
    "success": true,
    "filename": "test.jpg",
    "image_size": {
        "width": 1280,
        "height": 720
    },
    "detections": [
        {
            "class_id": 0,
            "class_name": "object",
            "confidence": 0.85,
            "bbox": {
                "x1": 100.5,
                "y1": 200.3,
                "x2": 150.8,
                "y2": 250.1
            }
        }
    ],
    "detection_count": 1
}
```

### 互動式文檔

啟動 API 後，訪問 **http://localhost:8000/docs** 查看完整的 Swagger UI 文檔。

---

## 專案結構

```
YOLO_Project/
├── .agents/                      # AI Agent 專家系統（37 個）
│   ├── backend_architect.md     # 後端架構設計
│   ├── fastapi_specialist.md    # FastAPI 開發
│   ├── python_perf_specialist.md # 效能優化
│   ├── code_review_specialist.md # 代碼審查
│   ├── debugging_specialist.md  # 除錯專家
│   └── ...                      # 其他 32 個專家
│
├── .claude/                      # Claude Code 設定
│   ├── commands/                 # 自定義命令（10 個）
│   │   ├── train.md             # 啟動訓練
│   │   ├── api-test.md          # 測試 API
│   │   ├── preprocess.md        # 資料預處理
│   │   ├── check-model.md       # 檢查模型
│   │   ├── start-services.md    # 啟動服務
│   │   ├── stop-services.md     # 停止服務
│   │   ├── validate.md          # 驗證模型
│   │   ├── commit-push.md       # Git 工作流程
│   │   ├── quick-predict.md     # 快速推論
│   │   └── project-status.md    # 專案狀態
│   ├── hooks/                   # 開發 Hooks（4 個）
│   │   ├── pre_train_validator.py     # 訓練前驗證
│   │   ├── api_startup_validator.py   # API 啟動驗證
│   │   ├── git_commit_validator.py    # Git 提交驗證
│   │   ├── hook_wrapper.py            # Hook 包裝器
│   │   └── README.md                  # Hooks 說明
│   ├── plugins/                 # 專業插件（4 個）
│   │   ├── dataset-analyzer/    # 資料集分析工具
│   │   ├── model-optimizer/     # 模型優化建議
│   │   ├── api-security/        # API 安全檢查
│   │   ├── training-monitor/    # 訓練監控工具
│   │   └── README.md            # Plugins 總覽
│   ├── skills/                  # 專案技能（3 個）
│   │   ├── backend-api/         # FastAPI 後端規範
│   │   ├── data-pipeline/       # 資料處理流程
│   │   └── yolo-training/       # YOLO 訓練流程
│   └── settings.json            # Claude Code 設定
│
├── config/                       # 配置檔（.gitignore）
│   ├── data.example.yaml        # 資料集配置範本 ⭐
│   ├── data.yaml                # 資料集配置（本地）
│   └── data_gray.yaml           # 灰階資料集配置（本地）
│
├── dataset/                      # 資料集目錄（.gitignore）
│   ├── your_dataset/            # 你的資料集
│   │   ├── images/              # 圖片檔案
│   │   │   ├── train/          # 訓練集圖片
│   │   │   └── val/            # 驗證集圖片
│   │   └── labels/              # 標註檔案
│   │       ├── train/          # 訓練集標註 (.txt)
│   │       └── val/            # 驗證集標註 (.txt)
│   └── README.md                # 資料集說明
│
├── runs/                         # 訓練輸出（.gitignore）
│   └── train/exp/
│       ├── weights/
│       │   ├── best.pt          # 最佳模型
│       │   └── last.pt          # 最後模型
│       ├── results.csv          # 訓練指標
│       └── results.png          # 訓練曲線
│
├── analysis/                     # Plugin 輸出（.gitignore）
├── monitoring/                   # Plugin 輸出（.gitignore）
├── optimization/                 # Plugin 輸出（.gitignore）
├── security/                     # Plugin 輸出（.gitignore）
│
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI 主程式
│   │   ├── test_api.py          # API 測試腳本
│   │   ├── requirements.txt     # Python 依賴
│   │   └── README.md            # API 文檔
│   ├── frontend/
│   │   ├── index.html           # Web UI
│   │   ├── app.js               # 前端邏輯
│   │   ├── start_frontend.sh    # 啟動腳本
│   │   └── README.md            # 前端文檔
│   ├── training/
│   │   └── train.py             # 訓練腳本
│   └── utils/
│       └── preprocess.py        # 資料預處理
│
├── .gitignore                    # Git 忽略規則
├── ARCHITECTURE.md               # 系統架構文檔
├── CLAUDE.md                     # 開發規範 ⭐
├── USAGE.md                      # 詳細使用指南
├── README.md                     # 本文件
├── README_AGENTS.md              # AI Agent 專家名錄 🤖
├── check_services.py             # 服務狀態檢查工具
├── start_all.sh                  # 啟動所有服務
└── stop_all.sh                   # 停止所有服務
```

### 目錄說明

#### 核心目錄
- **`.agents/`** - AI Agent 專家系統，包含 37 個專業領域 Agent（詳見 [README_AGENTS.md](README_AGENTS.md)）
- **`.claude/`** - Claude Code 整合，包含 10 個命令、4 個專業插件、4 個開發 Hooks
- **`src/`** - 程式碼目錄（API、前端、訓練、工具）
- **`config/`** - 配置檔案（⚠️ 不會被 commit，需自行建立）
- **`dataset/`** - 資料集目錄（⚠️ 不會被 commit，需自行準備）

#### 輸出目錄（自動生成，已在 .gitignore）
- **`runs/`** - YOLO 訓練結果和模型權重
- **`analysis/`** - Dataset Analyzer 輸出報告
- **`monitoring/`** - Training Monitor 監控日誌
- **`optimization/`** - Model Optimizer 分析結果
- **`security/`** - API Security 掃描報告

#### 文檔檔案
- **`README.md`** - 專案總覽和快速開始（本文件）
- **`README_AGENTS.md`** - AI Agent 專家名錄（🤖 包含 37 個專業 Agent）
- **`CLAUDE.md`** - 開發規範和 Git 規則（⭐ 必讀）
- **`ARCHITECTURE.md`** - 系統架構設計文檔
- **`USAGE.md`** - 詳細使用指南和工作流程

#### 工具腳本
- **`check_services.py`** - 服務狀態檢查工具
- **`start_all.sh`** - 啟動所有服務
- **`stop_all.sh`** - 停止所有服務

### 首次設定

**1. 準備配置檔案：**
```bash
cp config/data.example.yaml config/data.yaml
# 編輯 data.yaml，將路徑改為你的實際路徑
```

**2. 準備資料集：**
將你的資料集放入 `dataset/` 目錄，確保結構如下：
```
dataset/your_dataset/
├── images/train/    # 訓練圖片
├── images/val/      # 驗證圖片
├── labels/train/    # 訓練標註
└── labels/val/      # 驗證標註
```

**3. 使用 Claude Code Commands：**
```bash
/preprocess          # 預處理資料
/train               # 開始訓練
/project-status      # 查看狀態
```

---

## 技術棧

### 核心框架
- **[Ultralytics YOLO](https://github.com/ultralytics/ultralytics)** - 物件偵測引擎
- **[PyTorch](https://pytorch.org/)** - 深度學習框架
- **[FastAPI](https://fastapi.tiangolo.com/)** - 現代 Python Web 框架
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI 伺服器

### 前端
- **HTML5** + **CSS3** - 結構與樣式
- **Vanilla JavaScript** - 無框架依賴
- **Canvas API** - 結果視覺化

### 工具與套件
- **Pillow** - 圖片處理
- **NumPy** - 數值運算
- **Python Multipart** - 檔案上傳處理

---

## 效能指標

### 訓練效能
- **訓練速度**: ~2秒/epoch（29 張圖片，batch=8，MPS）
- **模型大小**: 5.5MB（best.pt）
- **記憶體使用**: ~2GB（訓練時）

### 推論效能
- **回應時間**: 100-300ms（含網路傳輸）
- **推論速度**: ~100ms/image（640x640，MPS）
- **吞吐量**: 5-10 請求/秒（單 worker）

### 前端效能
- **首次載入**: <1s
- **圖片上傳**: 即時
- **結果渲染**: <100ms

---

## 常見問題

### 訓練相關

**Q: 訓練時記憶體不足怎麼辦？**
A: 降低 `--batch` 參數（如 4 或 2）或使用較小的 `--imgsz`（如 416）。

**Q: 如何使用 GPU 加速？**
A: PyTorch 會自動偵測可用的 GPU。確認已安裝 CUDA 版本的 PyTorch（NVIDIA GPU）或使用 MPS（Apple Silicon）。

**Q: 訓練效果不佳怎麼改善？**
A:
- 增加訓練資料量
- 使用 `--augment` 啟用資料增強
- 嘗試更大的模型（`--model s` 或 `m`）
- 調整學習率與訓練輪數

### API 相關

**Q: API 無法連接？**
A: 確認服務已啟動：`curl http://localhost:8000/health`

**Q: 前端顯示 CORS 錯誤？**
A: 後端已配置 CORS 允許所有來源。確認 API 端點 URL 正確。

**Q: 偵測結果不準確？**
A:
- 降低 `conf_threshold`（如 0.2）提高召回率
- 調整 `iou_threshold` 控制重疊框
- 檢查模型是否已正確載入

### 部署相關

**Q: 如何在生產環境部署？**
A: 參考 [USAGE.md](USAGE.md) 的部署指南，建議使用 Docker 或雲端平台（AWS、GCP、Azure）。

**Q: 可以同時處理多個請求嗎？**
A: 可以，啟動時增加 worker 數量：
```bash
uvicorn src.api.main:app --workers 4
```

---

## 開發規範

本專案遵循以下開發規範（詳見 [CLAUDE.md](CLAUDE.md)）：

- **Python 風格**: 遵循 PEP8，使用 Type Hints
- **Git 規則**: 不 commit 模型檔（`.pt`）與資料集圖片
- **測試**: 新增功能需撰寫 `pytest` 測試

---

## 🤖 AI Agent 專家系統

本專案整合了 **37 個專業領域 AI Agent**，涵蓋軟體開發的各個面向，讓您在遇到特定問題時能夠召喚對應的專家協助。

### Agent 類別

| 類別 | Agent 數量 | 涵蓋領域 |
|------|-----------|---------|
| 🏗️ 架構與設計 | 4 個 | 後端架構、API 設計、資安威脅建模、雲端成本優化 |
| 🎨 前端與視覺 | 4 個 | React Native、Tailwind CSS、BI 儀表板、數據簡報 |
| ⚙️ 後端核心 | 3 個 | FastAPI、Go 併發、流程編排 |
| 💾 數據工程 | 5 個 | Event Sourcing、投影、dbt、資料品質、量化回測 |
| 🚀 效能優化 | 4 個 | Python 效能、非同步、SQL 優化、除錯 |
| 🛡️ 品管測試 | 3 個 | 代碼審查、單元測試、整合測試 |
| 🔧 DevOps | 5 個 | CI/CD、GitHub Actions、金鑰管理、Python 打包 |
| 🏴‍☠️ 資安逆向 | 4 個 | 協定分析、二進位分析、記憶體鑑識、反逆向 |

### 如何使用 Agent

當遇到特定領域的問題時，使用 `/add` 命令呼叫對應的專家：

```bash
# 範例 1：需要優化 API 效能
/add .agents/python_perf_specialist.md

# 範例 2：需要代碼審查
/add .agents/code_review_specialist.md

# 範例 3：設計系統架構
/add .agents/backend_architect.md
```

### Agent 組合技

對於複雜任務，可以依序呼叫多個 Agent：

```bash
# 完整開發流程
/add .agents/backend_architect.md      # 1. 規劃架構
/add .agents/fastapi_specialist.md     # 2. 實作功能
/add .agents/code_review_specialist.md # 3. 代碼審查
/add .agents/python_testing_specialist.md # 4. 撰寫測試
```

### Agent 名錄

完整的 Agent 清單與使用時機，請參閱 [README_AGENTS.md](README_AGENTS.md)。

---

## 🛠️ 開發工具

### 服務狀態檢查

快速檢查 API 和前端服務是否正常運行：

```bash
python3 check_services.py
```

**功能特色：**
- ✅ 檢查 API 服務健康狀態
- ✅ 檢查前端服務可用性
- ✅ 顯示服務 URL 和狀態資訊
- ✅ 回傳適當的 exit code（可用於腳本）

### 開發 Hooks

專案配置了 4 個自動化 Hook，在執行特定操作時自動驗證：

1. **pre_train_validator** - 訓練前檢查資料集、配置、依賴
2. **api_startup_validator** - API 啟動前檢查模型、端口、依賴
3. **git_commit_validator** - Git 提交前防止大型檔案和敏感資訊
4. **command_suggestion** - 推薦更好的工具和命令

這些 Hook 會在 Claude Code 執行對應命令時自動觸發，確保操作的安全性和正確性。

---

## 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 如何貢獻

1. Fork 本專案
2. 建立功能分支（`git checkout -b feature/amazing-feature`）
3. 提交變更（`git commit -m 'Add amazing feature'`）
4. 推送到分支（`git push origin feature/amazing-feature`）
5. 開啟 Pull Request

### 報告問題

如發現 Bug 或有功能建議，請在 [Issues](../../issues) 頁面提交。

---

## 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

---

## 聯絡資訊

- **GitHub**: [a23444452](https://github.com/a23444452)
- **Email**: a23444452@gmail.com

---

## 致謝

- [Ultralytics](https://github.com/ultralytics/ultralytics) - YOLO 實作
- [FastAPI](https://fastapi.tiangolo.com/) - 現代 Web 框架
- [Claude Code](https://github.com/anthropics/claude-code) - 開發輔助工具

---

<div align="center">

**Built with ❤️ using YOLO11n**

[⬆ 回到頂部](#yolo-物件偵測系統)

</div>
