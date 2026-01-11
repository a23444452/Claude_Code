#!/usr/bin/env python3
"""
Git Commit Validator Hook

在執行 git commit 前檢查，防止提交不應該被追蹤的檔案：
1. 模型權重檔案 (*.pt)
2. 資料集圖片
3. 配置檔案（非 example）
4. 大型檔案 (>10MB)
5. 敏感資訊

Exit codes:
  0 - 檢查通過
  1 - JSON 解析錯誤
  2 - 驗證失敗，阻止 commit
"""

import json
import os
import re
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


def get_staged_files():
    """取得已暫存的檔案列表"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []


def check_model_files(files):
    """檢查是否包含模型權重檔案"""
    model_files = [f for f in files if f.endswith('.pt')]
    if model_files:
        return False, f"發現模型權重檔案：\n  " + "\n  ".join(model_files) + "\n\n⚠️  模型檔案不應該被 commit（已在 .gitignore）\n建議：使用 git restore --staged <file> 取消暫存"
    return True, None


def check_dataset_files(files):
    """檢查是否包含資料集檔案"""
    dataset_patterns = [
        r'^dataset/.*\.(jpg|jpeg|png|bmp|gif)$',
        r'^dataset/.*\.txt$',
    ]

    dataset_files = []
    for f in files:
        for pattern in dataset_patterns:
            if re.match(pattern, f):
                dataset_files.append(f)
                break

    if dataset_files:
        return False, f"發現資料集檔案：\n  " + "\n  ".join(dataset_files[:5]) + \
               (f"\n  ... 還有 {len(dataset_files)-5} 個檔案" if len(dataset_files) > 5 else "") + \
               "\n\n⚠️  資料集不應該被 commit（已在 .gitignore）\n建議：使用 git restore --staged dataset/ 取消暫存"
    return True, None


def check_config_files(files):
    """檢查是否包含非 example 的配置檔案"""
    config_files = [f for f in files if f.startswith('config/') and f.endswith('.yaml') and 'example' not in f]

    if config_files:
        return False, f"發現本地配置檔案：\n  " + "\n  ".join(config_files) + "\n\n⚠️  本地配置包含路徑資訊，不應該被 commit\n建議：只 commit config/*.example.yaml 範本檔案"
    return True, None


def check_large_files(files):
    """檢查是否包含大型檔案 (>10MB)"""
    # 嘗試找到專案根目錄
    project_root = find_project_root()
    if not project_root:
        return True, None  # 找不到根目錄時跳過檢查

    large_files = []
    for f in files:
        file_path = project_root / f
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            if size_mb > 10:
                large_files.append(f"{f} ({size_mb:.1f}MB)")

    if large_files:
        return False, f"發現大型檔案：\n  " + "\n  ".join(large_files) + "\n\n⚠️  大型檔案不適合 Git 管理\n建議：使用 Git LFS 或雲端儲存"
    return True, None


def check_sensitive_info(files):
    """檢查是否包含敏感資訊檔案"""
    sensitive_patterns = [
        r'\.env$',
        r'\.env\.local$',
        r'secrets',
        r'credentials',
        r'password',
    ]

    sensitive_files = []
    for f in files:
        for pattern in sensitive_patterns:
            if re.search(pattern, f, re.IGNORECASE):
                sensitive_files.append(f)
                break

    if sensitive_files:
        return False, f"發現敏感資訊檔案：\n  " + "\n  ".join(sensitive_files) + "\n\n🚨 敏感資訊不應該被 commit！\n建議：立即取消暫存並加入 .gitignore"
    return True, None


def check_readme_updated(files):
    """檢查重大變更是否更新了 README.md"""
    # 定義重大變更的檔案類型
    significant_changes = [
        f for f in files
        if (f.startswith('src/') or f.startswith('.claude/'))
        and (f.endswith('.py') or f.endswith('.md'))
        and 'test' not in f
    ]

    readme_updated = 'README.md' in files

    if significant_changes and not readme_updated:
        # 這是警告，不阻止 commit，只提醒
        print("\n💡 提醒：你修改了以下重要檔案：", file=sys.stderr)
        for f in significant_changes[:3]:
            print(f"  - {f}", file=sys.stderr)
        if len(significant_changes) > 3:
            print(f"  ... 還有 {len(significant_changes)-3} 個檔案", file=sys.stderr)
        print("\n考慮是否需要更新 README.md 以反映這些變更。", file=sys.stderr)
        print("（參考 CLAUDE.md 的 Documentation Rules）\n", file=sys.stderr)

    return True, None


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    # 檢查是否是 git commit 命令
    tool_name = input_data.get("tool", {}).get("name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = input_data.get("tool", {}).get("input", {}).get("command", "")

    if "git commit" not in command:
        sys.exit(0)

    print("🔍 執行 Git Commit 檢查...\n", file=sys.stderr)

    # 取得暫存的檔案
    staged_files = get_staged_files()

    if not staged_files:
        print("⚠️  沒有暫存的檔案\n", file=sys.stderr)
        sys.exit(0)

    print(f"📝 檢查 {len(staged_files)} 個暫存檔案...\n", file=sys.stderr)

    # 執行所有檢查
    checks = [
        ("模型檔案", check_model_files),
        ("資料集檔案", check_dataset_files),
        ("配置檔案", check_config_files),
        ("大型檔案", check_large_files),
        ("敏感資訊", check_sensitive_info),
        ("文檔更新", check_readme_updated),
    ]

    all_passed = True
    for check_name, check_func in checks:
        passed, error_msg = check_func(staged_files)
        if passed:
            print(f"✅ {check_name}: 通過", file=sys.stderr)
        else:
            print(f"❌ {check_name}: 失敗", file=sys.stderr)
            print(f"   {error_msg}\n", file=sys.stderr)
            all_passed = False

    if not all_passed:
        print("\n⚠️  Git Commit 檢查未通過，請修正上述問題後再試。\n", file=sys.stderr)
        print("如果確定要提交，可以使用 --no-verify 跳過檢查（不建議）\n", file=sys.stderr)
        sys.exit(2)

    print("\n✅ 所有檢查通過，可以 commit！\n", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
