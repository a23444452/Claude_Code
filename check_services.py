#!/usr/bin/env python3
"""檢查服務狀態"""
import requests
import sys

def check_api():
    """檢查 API 服務"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API 服務: 運行中")
            print(f"   狀態: {data.get('status')}")
            print(f"   模型已載入: {data.get('model_loaded')}")
            return True
    except Exception as e:
        print(f"❌ API 服務: 無法連接 - {e}")
        return False

def check_frontend():
    """檢查前端服務"""
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print(f"✅ 前端服務: 運行中 (HTTP {response.status_code})")
            return True
    except Exception as e:
        print(f"❌ 前端服務: 無法連接 - {e}")
        return False

if __name__ == "__main__":
    print("🔍 檢查服務狀態...\n")

    api_ok = check_api()
    print()
    frontend_ok = check_frontend()
    print()

    if api_ok and frontend_ok:
        print("✅ 所有服務運行正常！\n")
        print("🌐 前端介面: http://localhost:3000")
        print("🔌 後端 API:  http://localhost:8000")
        print("📚 API 文檔:  http://localhost:8000/docs")
        sys.exit(0)
    else:
        print("⚠️  部分服務未運行")
        sys.exit(1)
