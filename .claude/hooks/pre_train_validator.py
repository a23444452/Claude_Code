#!/usr/bin/env python3
"""
Pre-Training Validator Hook

在執行訓練前檢查必要條件，確保：
1. 資料集已準備好
2. 配置檔案存在
3. 必要的依賴已安裝
4. 沒有正在運行的訓練

Exit codes:
  0 - 檢查通過，可以訓練
  1 - JSON 解析錯誤
  2 - 驗證失敗，阻止訓練
"""

import json
import os
import re
import sys
from pathlib import Path


def find_project_root():
    """尋找專案根目錄（包含 .claude 目錄）"""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".claude").exists():
            return current
        current = current.parent
    return None


def check_dataset_exists():
    """檢查資料集目錄是否存在"""
    # 嘗試找到專案根目錄
    project_root = find_project_root()
    if not project_root:
        return True, None  # 找不到根目錄時跳過檢查

    dataset_dir = project_root / "dataset"
    if not dataset_dir.exists():
        return False, "資料集目錄不存在：dataset/"

    # 檢查是否有任何資料集子目錄
    subdirs = [d for d in dataset_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    if not subdirs:
        return False, "dataset/ 目錄下沒有資料集"

    return True, None


def check_config_exists():
    """檢查配置檔案是否存在"""
    # 嘗試找到專案根目錄
    project_root = find_project_root()
    if not project_root:
        return True, None  # 找不到根目錄時跳過檢查

    config_dir = project_root / "config"
    if not config_dir.exists():
        return False, "config/ 目錄不存在"

    config_files = list(config_dir.glob("*.yaml"))
    if not config_files:
        return False, "config/ 目錄下沒有 .yaml 配置檔案\n提示：複製 config/data.example.yaml 並修改"

    # 檢查是否只有 example 檔案
    non_example_configs = [f for f in config_files if 'example' not in f.name]
    if not non_example_configs:
        return False, "只找到 example 配置檔案，請建立實際的配置檔\n提示：cp config/data.example.yaml config/data.yaml"

    return True, None


def check_training_in_progress():
    """檢查是否已有訓練在進行"""
    import subprocess
    try:
        result = subprocess.run(
            ["pgrep", "-f", "train.py"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            return False, "已有訓練程序在運行中（PID: {}）\n建議：使用 /training-monitor --watch 監控現有訓練".format(result.stdout.strip())
    except FileNotFoundError:
        # pgrep 不存在（Windows），跳過檢查
        pass

    return True, None


def check_dependencies():
    """檢查必要的 Python 套件是否已安裝"""
    required_packages = ['ultralytics', 'torch', 'PIL']
    missing = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        return False, f"缺少必要的套件：{', '.join(missing)}\n安裝：pip install -r src/api/requirements.txt"

    return True, None


def main():
    try:
        # 讀取 stdin 的 JSON 輸入
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    # 檢查是否是訓練相關的命令
    tool_name = input_data.get("tool", {}).get("name", "")
    if tool_name != "Bash":
        # 不是 Bash 命令，直接通過
        sys.exit(0)

    command = input_data.get("tool", {}).get("input", {}).get("command", "")

    # 檢查是否是訓練命令
    is_training_command = (
        "train.py" in command or
        "/train" in command or
        "yolo train" in command
    )

    if not is_training_command:
        # 不是訓練命令，直接通過
        sys.exit(0)

    print("🔍 執行訓練前檢查...\n", file=sys.stderr)

    # 執行所有檢查
    checks = [
        ("資料集", check_dataset_exists),
        ("配置檔案", check_config_exists),
        ("訓練狀態", check_training_in_progress),
        ("依賴套件", check_dependencies),
    ]

    all_passed = True
    for check_name, check_func in checks:
        passed, error_msg = check_func()
        if passed:
            print(f"✅ {check_name}: 通過", file=sys.stderr)
        else:
            print(f"❌ {check_name}: 失敗", file=sys.stderr)
            print(f"   {error_msg}\n", file=sys.stderr)
            all_passed = False

    if not all_passed:
        print("\n⚠️  訓練前檢查未通過，請修正上述問題後再試。\n", file=sys.stderr)
        sys.exit(2)  # 阻止執行

    print("\n✅ 所有檢查通過，開始訓練！\n", file=sys.stderr)
    sys.exit(0)  # 允許執行


if __name__ == "__main__":
    main()
