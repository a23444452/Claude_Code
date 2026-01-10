# Claude Plugin Marketplace - YOLO Project

本目錄包含 YOLO 物件偵測專案的 Claude Code 插件集合，提供訓練、部署、優化等各方面的專業協助。

## 📦 Plugin 列表

### 🎯 開發類 (Development)

#### 1. **yolo-training-advisor** - 訓練顧問
協助優化訓練超參數、診斷過擬合/欠擬合問題。

**使用時機**:
- 開始新的訓練
- Loss 不下降
- 過擬合問題
- 需要加速訓練

**範例**:
```
User: 我的模型過擬合了，該怎麼辦？
Plugin: [提供資料增強、early stopping、正則化建議]
```

---

#### 2. **dataset-quality-guard** - 資料集品質守衛
驗證 YOLO 格式資料集，檢查標註錯誤和類別分布。

**使用時機**:
- 訓練前必須執行
- 新增資料後
- 訓練效果不佳

**範例**:
```
User: 驗證我的資料集 config/data.yaml
Plugin: [執行完整驗證，報告問題和建議]
```

---

#### 4. **model-deployment-assistant** - 部署助手
協助將模型匯出為不同格式（ONNX, TensorRT, CoreML）。

**支援格式**:
- ONNX (通用)
- TensorRT (NVIDIA GPU)
- CoreML (Apple)
- TFLite (Mobile)

---

#### 7. **data-augmentation-tuner** - 資料增強調校器
根據資料集大小推薦最佳增強策略。

---

### ⚡ 生產力類 (Productivity)

#### 3. **api-performance-optimizer** - API 效能優化器
分析 FastAPI 效能瓶頸，提供快取、批次處理建議。

**優化項目**:
- 模型載入
- 批次處理
- 快取策略
- 並發請求

---

#### 5. **training-monitor** - 訓練監控
即時追蹤訓練指標，偵測異常。

**監控指標**:
- Loss, mAP, Precision, Recall
- GPU/Memory 使用率

---

#### 8. **inference-optimizer** - 推論優化器
提升預測速度和準確度平衡。

**優化技術**:
- Batch inference
- Confidence threshold
- Image size tuning

---

#### 10. **model-comparison-tool** - 模型比較工具
比較不同 YOLO 變體，推薦最適合的模型。

**比較維度**:
- 大小、速度、準確度
- 硬體需求
- 使用場景

---

### 🔒 安全類 (Security)

#### 6. **yolo-security-advisor** - 安全顧問
API 安全最佳實踐，防止常見漏洞。

**安全檢查**:
- 檔案上傳驗證
- 速率限制
- 輸入驗證
- CORS 配置

---

### 📚 學習類 (Learning)

#### 9. **yolo-learning-assistant** - 學習助手
互動式教學，解釋 YOLO 概念和原理。

**主題**:
- YOLO 基礎
- 訓練概念
- 效能指標
- 最佳實踐

---

## 🚀 快速開始

### 安裝 Plugins

Plugins 已包含在專案中，Claude Code 會自動載入。

### 使用 Plugin

在 Claude Code 對話中直接提問：

```
# 訓練相關
"幫我優化訓練參數"
"為什麼我的模型過擬合？"

# 資料集相關
"驗證我的資料集"
"類別分布是否平衡？"

# API 相關
"如何優化 API 效能？"
"實作批次推論"

# 部署相關
"匯出模型為 ONNX"
"如何在 Raspberry Pi 部署？"

# 學習相關
"什麼是 mAP？"
"YOLO 如何運作？"
```

---

## 📖 Plugin 使用指南

### 工作流程範例

#### 訓練前準備
```
1. dataset-quality-guard: 驗證資料集
   ↓
2. yolo-training-advisor: 規劃訓練策略
   ↓
3. data-augmentation-tuner: 設定增強參數
   ↓
4. model-comparison-tool: 選擇模型大小
```

#### 訓練過程
```
1. training-monitor: 監控訓練進度
   ↓
2. yolo-training-advisor: 調整超參數
   ↓
3. (訓練完成)
```

#### 部署流程
```
1. model-deployment-assistant: 選擇匯出格式
   ↓
2. inference-optimizer: 優化推論速度
   ↓
3. api-performance-optimizer: 設計 API
   ↓
4. yolo-security-advisor: 實作安全措施
```

---

## 🎯 常見使用場景

### 場景 1: 新專案開始
```
1. "幫我規劃 YOLO 訓練流程"
   → yolo-training-advisor 提供完整計畫

2. "驗證我的資料集"
   → dataset-quality-guard 檢查品質

3. "選擇適合的模型"
   → model-comparison-tool 推薦模型
```

### 場景 2: 訓練效果不佳
```
1. "為什麼 Loss 不下降？"
   → yolo-training-advisor 診斷問題

2. "檢查資料集品質"
   → dataset-quality-guard 找出問題

3. "優化資料增強"
   → data-augmentation-tuner 調整參數
```

### 場景 3: API 開發
```
1. "設計 YOLO API"
   → api-performance-optimizer 提供架構

2. "實作安全檢查"
   → yolo-security-advisor 提供範例

3. "優化推論速度"
   → inference-optimizer 提供策略
```

### 場景 4: 部署到生產
```
1. "匯出模型"
   → model-deployment-assistant 指導匯出

2. "優化推論"
   → inference-optimizer 調整參數

3. "監控效能"
   → api-performance-optimizer 設定監控
```

---

## 🔧 Plugin 配置

### marketplace.json 結構
```json
{
  "name": "yolo-project-plugins",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "plugin-name",
      "description": "Plugin description",
      "source": "plugin-file.md",
      "category": "development|productivity|security|learning"
    }
  ]
}
```

### 自訂 Plugin

建立新的 `.md` 檔案：

```markdown
# My Custom Plugin

## Description
Plugin 簡介

## Capabilities
- 功能 1
- 功能 2

## Usage
使用範例
```

然後在 `marketplace.json` 註冊：
```json
{
  "name": "my-custom-plugin",
  "description": "My plugin",
  "source": "my-custom-plugin.md",
  "category": "development"
}
```

---

## 💡 最佳實踐

### 1. 訓練前必用
- `dataset-quality-guard` - 驗證資料集
- `yolo-training-advisor` - 規劃策略

### 2. 訓練中監控
- `training-monitor` - 追蹤指標
- `yolo-training-advisor` - 調整參數

### 3. API 開發必用
- `api-performance-optimizer` - 效能優化
- `yolo-security-advisor` - 安全檢查

### 4. 部署前檢查
- `model-deployment-assistant` - 選擇格式
- `inference-optimizer` - 優化推論

### 5. 學習 YOLO
- `yolo-learning-assistant` - 概念學習
- `model-comparison-tool` - 模型比較

---

## ❓ 常見問題

### Q: 如何啟用 Plugin？
A: Plugins 自動載入，直接在 Claude Code 中提問即可。

### Q: Plugin 可以同時使用嗎？
A: 可以！Plugins 互補，建議搭配使用。

### Q: 如何知道該用哪個 Plugin？
A: 參考上方的使用場景，或直接描述問題讓 Claude 選擇。

### Q: Plugin 會自動執行嗎？
A: 不會，Plugins 是對話式輔助，需要你的提問觸發。

### Q: 可以建立自己的 Plugin 嗎？
A: 可以！參考現有 plugin 格式建立 `.md` 檔案並註冊。

---

## 📊 Plugin 分類概覽

### 按類別
- **Development** (5): 訓練、資料集、部署、增強、學習
- **Productivity** (4): API、監控、推論、比較
- **Security** (1): 安全顧問
- **Learning** (1): 學習助手

### 按使用頻率
- **訓練必用**: dataset-quality-guard, yolo-training-advisor
- **API 必用**: api-performance-optimizer, yolo-security-advisor
- **部署必用**: model-deployment-assistant, inference-optimizer
- **學習工具**: yolo-learning-assistant, model-comparison-tool

---

## 🔗 相關資源

### 專案文檔
- [README.md](../README.md) - 專案總覽
- [CLAUDE.md](../CLAUDE.md) - 開發規範
- [.claude/plugins/](../.claude/plugins/) - 其他 plugins
- [.claude/commands/](../.claude/commands/) - Claude 命令

### 工具
- [scripts/](../scripts/) - 實用腳本
- [.vscode/](../.vscode/) - VS Code 配置
- [.devcontainer/](../.devcontainer/) - Dev Container

---

## 🎉 總結

Claude Plugin 集合提供全方位的 YOLO 開發支援：

✅ **10 個專業 Plugins** - 涵蓋訓練、API、部署、安全
✅ **分類清晰** - Development, Productivity, Security, Learning
✅ **即問即答** - 對話式交互，簡單直觀
✅ **工作流程整合** - 與專案工具無縫配合
✅ **最佳實踐** - 內建專業知識和經驗

**開始使用**: 直接在 Claude Code 中提問，例如 "幫我驗證資料集" 或 "如何優化訓練？"

祝開發順利！🚀
