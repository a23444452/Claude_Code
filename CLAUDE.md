# YOLO Image Recognition Project

## Project Overview
這是一個基於 YOLO (You Only Look Once) 的影像辨識系統。
目標：即時偵測 [你的目標物件，例如：工安帽、瑕疵產品]。

## Tech Stack
- **Core**: Python 3.10+, PyTorch, Ultralytics YOLOv8/v11
- **Backend**: FastAPI, Uvicorn
- **Frontend**: [你的選擇，如 Streamlit 或 React]
- **Deployment**: Docker, Nginx

## Key Directories
- `dataset/` - 原始圖片與標註檔 (YOLO format: *.txt)
- `models/` - 訓練好的權重檔 (*.pt)
- `src/training/` - 訓練與微調腳本
- `src/api/` - 後端 API 程式碼
- `src/frontend/` - 前端介面程式碼

## Development Rules
- **Python Style**: 遵循 PEP8，必須使用 Type Hints。
- **Git Rules**: 不要 commit `.pt` 模型大檔或 `dataset/` 下的圖片。
- **Testing**: 新增功能需撰寫 `pytest` 測試。
