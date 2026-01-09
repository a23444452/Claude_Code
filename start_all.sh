#!/bin/bash
# 一鍵啟動 YOLO 物件偵測系統

echo "=========================================="
echo "🚀 YOLO 物件偵測系統啟動中..."
echo "=========================================="
echo ""

# 設定專案路徑
PROJECT_DIR="/Users/vincewang/YOLO_Project"
cd "$PROJECT_DIR"

# 檢查環境
echo "📋 檢查環境..."
if [ ! -d "~/miniforge3/envs/YOLO_env" ]; then
    echo "❌ 找不到 YOLO_env 環境"
    exit 1
fi

if [ ! -f "runs/train/exp/weights/best.pt" ]; then
    echo "⚠️  找不到訓練好的模型，將使用預訓練模型"
fi

echo "✅ 環境檢查完成"
echo ""

# 啟動後端 API
echo "🔧 啟動後端 API (Port 8000)..."
~/miniforge3/envs/YOLO_env/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 > logs/api.log 2>&1 &
API_PID=$!
sleep 3

# 檢查 API 是否成功啟動
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 後端 API 啟動成功"
else
    echo "❌ 後端 API 啟動失敗"
    exit 1
fi
echo ""

# 啟動前端服務
echo "🎨 啟動前端服務 (Port 3000)..."
cd src/frontend
python3 -m http.server 3000 > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd "$PROJECT_DIR"
sleep 2

# 檢查前端是否成功啟動
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ 前端服務啟動成功"
else
    echo "❌ 前端服務啟動失敗"
    exit 1
fi
echo ""

# 顯示資訊
echo "=========================================="
echo "✅ 系統啟動成功！"
echo "=========================================="
echo ""
echo "🌐 前端介面: http://localhost:3000"
echo "🔌 後端 API:  http://localhost:8000"
echo "📚 API 文檔:  http://localhost:8000/docs"
echo ""
echo "📝 日誌位置:"
echo "   - 後端: logs/api.log"
echo "   - 前端: logs/frontend.log"
echo ""
echo "🛑 停止服務:"
echo "   kill $API_PID $FRONTEND_PID"
echo ""
echo "或執行: ./stop_all.sh"
echo "=========================================="
echo ""

# 儲存 PID 以便後續停止
echo "$API_PID" > .api.pid
echo "$FRONTEND_PID" > .frontend.pid

# 開啟瀏覽器（macOS）
if command -v open &> /dev/null; then
    echo "🌍 正在開啟瀏覽器..."
    sleep 1
    open http://localhost:3000
fi

echo ""
echo "按 Ctrl+C 檢視日誌，或直接使用系統"
echo ""

# 持續執行（可選）
# wait
