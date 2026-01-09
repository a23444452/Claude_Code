#!/bin/bash
# 啟動前端服務

echo "🚀 啟動 YOLO 物件偵測前端..."
echo ""
echo "前端服務: http://localhost:3000"
echo "後端 API: http://localhost:8000"
echo ""
echo "請確保後端 API 已啟動！"
echo "按 Ctrl+C 停止服務"
echo ""

cd "$(dirname "$0")"
python3 -m http.server 3000
