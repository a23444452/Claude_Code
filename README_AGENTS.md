# 🤖 Project Agents Directory (虛擬專家名錄)

這份文件列出了本專案中所有可用的 AI Agent。當遇到特定領域的難題時，請使用 `/add .agents/{filename}` 呼叫對應專家。

---

## 🏗️ 1. 架構與設計 (Architecture & Design)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `backend_architect.md` | **後端總架構師** | 專案剛開始，需要規劃整體系統、選型 (SQL vs NoSQL)、分層架構時。 |
| `api_design_specialist.md` | **API 設計師** | 定義前後端介面 (Contract) 時，需要寫 OpenAPI/Swagger 規格。 |
| `stride_specialist.md` | **資安架構師** | 系統設計階段，想找出架構有沒有邏輯漏洞或被攻擊的風險 (威脅建模)。 |
| `cloud_cost_specialist.md` | **FinOps 財務官** | 覺得雲端費用太貴，或開機器前需要評估預算與省錢方案。 |

## 🎨 2. 前端與視覺 (Frontend & Visuals)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `react_native_specialist.md` | **App 開發者** | 撰寫 Mobile App 邏輯、處理 State、Navigation。 |
| `tailwind_specialist.md` | **UI/UX 設計師** | 調整樣式、配色、RWD 排版、Dark Mode、Design System。 |
| `bi_dashboard_specialist.md` | **BI 分析師** | 設計儀表板版面，決定要看什麼 KPI，如何呈現數據才易讀。 |
| `data_storyteller.md` | **簡報專家** | 做完圖表後，要向老闆或客戶進行數據匯報與說服時。 |

## ⚙️ 3. 後端核心與流程 (Backend & Workflow)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `fastapi_specialist.md` | **Python API 開發** | 撰寫主要業務邏輯、RESTful API、整合 AI 模型。 |
| `go_concurrency_specialist.md` | **Go 系統工程師** | 處理超高併發連線 (如 IoT Gateway)、需要極致效能的微服務。 |
| `workflow_orchestrator.md` | **流程編排專家** | 設計跨服務的長流程 (Saga)，需要重試、補償機制 (Temporal)。 |

## 💾 4. 數據工程與量化 (Data & Quant)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `event_store_specialist.md` | **事件儲存專家** | 設計「寫入端」資料庫，實作 Event Sourcing (紀錄發生過的所有事)。 |
| `projection_specialist.md` | **投影專家** | 設計「讀取端」資料庫 (MongoDB/Redis)，為了讀取速度做資料攤平。 |
| `dbt_specialist.md` | **分析工程師** | 將原始資料 (Raw Data) 轉換成有意義的報表資料 (Data Models)。 |
| `data_quality_specialist.md` | **資料品質守門員** | 檢查資料是否乾淨 (Validation)，防止髒資料汙染 AI 模型或報表。 |
| `quant_backtest_specialist.md` | **量化研究員** | 驗證股票交易策略是否有效 (回測)，計算 Sharpe Ratio 與風險。 |

## 🚀 5. 效能與優化 (Performance & Optimization)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `python_perf_specialist.md` | **演算法優化** | Python 跑太慢 (CPU Bound)、記憶體爆掉、需要 NumPy 向量化加速。 |
| `async_python_specialist.md` | **非同步專家** | API 回應卡住 (Blocking)、高併發 I/O 請求處理。 |
| `sql_optimization_specialist.md` | **資料庫優化** | SQL 查詢太慢，需要分析 Query Plan 與建立索引。 |
| `debugging_specialist.md` | **除錯神探** | 程式跑不出來、結果錯誤，需要找 Root Cause (根本原因)。 |

## 🛡️ 6. 品管與測試 (QA & Testing)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `code_review_specialist.md` | **代碼審查員** | 寫完程式要 Commit 前，檢查風格、可讀性與潛在錯誤。 |
| `python_testing_specialist.md` | **單元測試專家** | 撰寫 Pytest，測試單一函數或類別的邏輯。 |
| `temporal_test_specialist.md` | **整合測試專家** | 測試長流程、時間跳躍 (Time Skipping)、模擬故障重試。 |

## 🔧 7. DevOps 與基礎建設 (DevOps & Infra)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `cicd_specialist.md` | **DevOps 策略** | 規劃自動化部署流程、版號管理、發布策略。 |
| `github_actions_specialist.md` | **YAML 工程師** | 撰寫 CI/CD 的 yaml 設定檔，處理 Cache 與自動化腳本。 |
| `secrets_specialist.md` | **金鑰管理員** | 確保 API Key 沒有寫死在程式碼裡，管理 `.env` 與憑證。 |
| `python_packaging_specialist.md` | **打包專家 (Poetry)** | 開發共用 Library，需要發布到 PyPI 供他人安裝。 |
| `uv_specialist.md` | **極速管理 (uv)** | 需要極致快速的安裝體驗、管理 Python 版本、跑腳本。 |

## 🏴‍☠️ 8. 逆向工程與攻防 (Reverse Engineering & Security)
| 檔案名稱 | 角色 | 什麼時候呼叫？(情境) |
| :--- | :--- | :--- |
| `protocol_re_specialist.md` | **協定分析師** | 想要控制沒有 API 文件的硬體，需要分析網路封包 (Wireshark)。 |
| `binary_analysis_specialist.md` | **二進位分析師** | 沒有 Source Code，需要分析 `.exe` 或 `.dll` 的邏輯或當機原因。 |
| `memory_forensics_specialist.md` | **記憶體鑑識官** | 程式正在跑但不知密碼，需要從 RAM 中提取 Key 或 Config。 |
| `anti_re_specialist.md` | **防護專家** | 保護自己的 Python 程式碼，防止被別人逆向或盜用。 |

---
> **Usage Tip**:
> - 組合技：`/add .agents/backend_architect.md` (規劃) -> `/add .agents/fastapi_specialist.md` (實作) -> `/add .agents/code_review_specialist.md` (檢查)。
> - 遇到困難時，隨時回來查閱此表。
