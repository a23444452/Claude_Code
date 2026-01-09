#!/bin/bash
# 停止所有服務

echo "=========================================="
echo "🛑 停止 YOLO 物件偵測系統..."
echo "=========================================="
echo ""

# 停止 API 服務
if [ -f .api.pid ]; then
    API_PID=$(cat .api.pid)
    if ps -p $API_PID > /dev/null 2>&1; then
        echo "🔧 停止後端 API (PID: $API_PID)..."
        kill $API_PID
        rm .api.pid
        echo "✅ 後端 API 已停止"
    fi
else
    echo "🔧 停止所有 uvicorn 進程..."
    pkill -f "uvicorn src.api.main:app"
fi

# 停止前端服務
if [ -f .frontend.pid ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "🎨 停止前端服務 (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm .frontend.pid
        echo "✅ 前端服務已停止"
    fi
else
    echo "🎨 停止所有 http.server 進程..."
    pkill -f "python3 -m http.server 3000"
fi

echo ""
echo "=========================================="
echo "✅ 所有服務已停止"
echo "=========================================="
