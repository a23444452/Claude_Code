#!/usr/bin/env python3
"""
API Startup Validator Hook

在啟動 API 服務前檢查：
1. 模型檔案是否存在
2. 端口是否已被佔用
3. 必要的依賴是否已安裝
4. 環境配置是否正確

Exit codes:
  0 - 檢查通過
  1 - JSON 解析錯誤
  2 - 驗證失敗，阻止啟動
"""

import json
import os
import re
import sys
import socket
import subprocess
from pathlib import Path


def find_project_root():
    """尋找專案根目錄（包含 .claude 目錄）"""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".claude").exists():
            return current
        current = current.parent
    return None


def check_model_exists():
    """檢查是否有訓練好的模型"""
    # 嘗試找到專案根目錄
    project_root = find_project_root()
    if not project_root:
        return True, None  # 找不到根目錄時跳過檢查

    # 檢查預訓練模型或訓練輸出的模型
    model_paths = [
        project_root / "yolo11n.pt",  # 預訓練模型
        project_root / "runs/train/exp/weights/best.pt",  # 訓練的最佳模型
    ]

    existing_models = [str(p) for p in model_paths if p.exists()]

    if not existing_models:
        return False, "找不到模型檔案\n建議：\n  1. 下載預訓練模型：yolo11n.pt\n  2. 或先訓練模型：/train"

    print(f"   找到模型：{existing_models[0]}", file=sys.stderr)
    return True, None


def check_port_available(port=8000):
    """檢查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('', port))
        sock.close()
        return True, None
    except OSError:
        return False, f"端口 {port} 已被佔用\n建議：\n  1. 停止現有服務：/stop-services\n  2. 或使用其他端口：uvicorn ... --port 8001"


def check_api_dependencies():
    """檢查 API 必要的依賴"""
    required = ['fastapi', 'uvicorn', 'PIL', 'ultralytics']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        return False, f"缺少 API 依賴：{', '.join(missing)}\n安裝：pip install -r src/api/requirements.txt"

    return True, None


def check_api_file_exists():
    """檢查 API 主檔案是否存在"""
    # 嘗試找到專案根目錄
    project_root = find_project_root()
    if not project_root:
        return True, None  # 找不到根目錄時跳過檢查

    api_file = project_root / "src/api/main.py"
    if not api_file.exists():
        return False, f"找不到 API 主檔案：{api_file}"

    return True, None


def check_cors_config():
    """檢查 CORS 配置（提醒而非阻止）"""
    # 嘗試找到專案根目錄
    project_root = find_project_root()
    if not project_root:
        return True, None  # 找不到根目錄時跳過檢查

    api_file = project_root / "src/api/main.py"
    if api_file.exists():
        content = api_file.read_text()
        if 'allow_origins=["*"]' in content:
            print("\n⚠️  警告：CORS 配置允許所有來源", file=sys.stderr)
            print("   生產環境建議限制特定域名", file=sys.stderr)
            print("   參考：/api-security 進行安全檢查\n", file=sys.stderr)

    return True, None


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    # 檢查是否是 API 啟動命令
    tool_name = input_data.get("tool", {}).get("name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = input_data.get("tool", {}).get("input", {}).get("command", "")

    is_api_command = (
        "uvicorn" in command or
        "src/api/main.py" in command or
        "start_all.sh" in command or
        "/start-services" in command
    )

    if not is_api_command:
        sys.exit(0)

    print("🔍 執行 API 啟動檢查...\n", file=sys.stderr)

    # 執行所有檢查
    checks = [
        ("API 檔案", check_api_file_exists),
        ("模型檔案", check_model_exists),
        ("端口可用性", lambda: check_port_available(8000)),
        ("API 依賴", check_api_dependencies),
        ("CORS 配置", check_cors_config),
    ]

    all_passed = True
    for check_name, check_func in checks:
        passed, error_msg = check_func()
        if passed:
            print(f"✅ {check_name}: 通過", file=sys.stderr)
        else:
            print(f"❌ {check_name}: 失敗", file=sys.stderr)
            if error_msg:
                print(f"   {error_msg}\n", file=sys.stderr)
            all_passed = False

    if not all_passed:
        print("\n⚠️  API 啟動檢查未通過，請修正上述問題後再試。\n", file=sys.stderr)
        sys.exit(2)

    print("\n✅ 所有檢查通過，啟動 API 服務！\n", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
