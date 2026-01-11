#!/usr/bin/env python3
"""
Hook Wrapper
自動找到專案根目錄並執行 hook 腳本
"""
import sys
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


def main():
    if len(sys.argv) < 2:
        print("Usage: hook_wrapper.py <hook_script_name>", file=sys.stderr)
        sys.exit(1)

    hook_name = sys.argv[1]

    # 找到專案根目錄
    project_root = find_project_root()
    if not project_root:
        # 找不到專案根目錄，直接通過
        sys.exit(0)

    # 建立 hook 腳本的完整路徑
    hook_script = project_root / ".claude" / "hooks" / hook_name

    if not hook_script.exists():
        print(f"Hook script not found: {hook_script}", file=sys.stderr)
        sys.exit(0)

    # 執行 hook 腳本，並傳遞 stdin
    try:
        result = subprocess.run(
            ["python3", str(hook_script)],
            stdin=sys.stdin,
            capture_output=True,
            text=True
        )

        # 輸出 stderr（hook 的輸出）
        if result.stderr:
            print(result.stderr, file=sys.stderr, end='')

        # 輸出 stdout（如果有）
        if result.stdout:
            print(result.stdout, end='')

        sys.exit(result.returncode)

    except Exception as e:
        print(f"Error executing hook: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
