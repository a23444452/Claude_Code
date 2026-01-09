#!/usr/bin/env python3
"""
Command Suggestion Hook

提供更好的命令建議，改善開發體驗：
1. 建議使用 Claude Code commands 替代原始命令
2. 提醒使用更高效的工具
3. 提供最佳實踐建議

Exit codes:
  0 - 允許執行（可能有建議）
  1 - JSON 解析錯誤
  2 - 阻止執行並提供替代方案
"""

import json
import re
import sys


def suggest_better_commands(command):
    """為常見命令提供更好的替代方案"""
    suggestions = []

    # 訓練相關
    if re.search(r'python.*train\.py', command):
        suggestions.append({
            'original': command,
            'better': '/train',
            'reason': 'Claude Code command 會自動檢查環境和資料集',
            'block': False
        })

    # API 測試
    if 'curl.*predict' in command or 'requests.*predict' in command:
        suggestions.append({
            'original': command,
            'better': '/api-test',
            'reason': '自動測試所有端點並顯示結果',
            'block': False
        })

    # 資料預處理
    if re.search(r'python.*preprocess\.py', command):
        suggestions.append({
            'original': command,
            'better': '/preprocess',
            'reason': '簡化的命令，自動檢查資料品質',
            'block': False
        })

    # 模型驗證
    if 'yolo val' in command or re.search(r'python.*validate', command):
        suggestions.append({
            'original': command,
            'better': '/validate',
            'reason': '統一的驗證流程，生成完整報告',
            'block': False
        })

    # Git 工作流程
    if 'git add' in command and 'git commit' in command and 'git push' in command:
        suggestions.append({
            'original': command,
            'better': '/commit-push',
            'reason': '自動執行 git 工作流程並檢查規範',
            'block': False
        })

    # 服務啟動
    if 'uvicorn' in command and 'start_frontend' in command:
        suggestions.append({
            'original': command,
            'better': '/start-services',
            'reason': '一次啟動所有服務（API + Frontend）',
            'block': False
        })

    # 專案狀態檢查
    if any(x in command for x in ['git status', 'ls -la', 'du -sh']):
        if 'git status' in command:
            suggestions.append({
                'original': command,
                'better': '/project-status',
                'reason': '查看完整的專案狀態（Git + 資料集 + 模型 + 服務）',
                'block': False
            })

    # 使用 find 而不是 Glob tool
    if re.match(r'find.*-name.*\.(py|yaml|txt)', command):
        suggestions.append({
            'original': command,
            'better': 'Glob tool',
            'reason': 'Claude Code 的 Glob tool 更快且更易用',
            'block': True
        })

    # 使用 cat/head/tail 而不是 Read tool
    if re.match(r'(cat|head|tail)\s+.*\.(py|yaml|txt|md)', command):
        suggestions.append({
            'original': command,
            'better': 'Read tool',
            'reason': 'Claude Code 的 Read tool 提供更好的格式化',
            'block': True
        })

    # 使用 grep 而不是 Grep tool
    if re.match(r'grep\s+-r', command):
        suggestions.append({
            'original': command,
            'better': 'Grep tool',
            'reason': 'Claude Code 的 Grep tool 更快（基於 ripgrep）',
            'block': True
        })

    return suggestions


def main():
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool", {}).get("name", "")
    if tool_name != "Bash":
        sys.exit(0)

    command = input_data.get("tool", {}).get("input", {}).get("command", "")

    # 檢查是否有更好的建議
    suggestions = suggest_better_commands(command)

    if not suggestions:
        sys.exit(0)

    # 顯示建議
    blocking_suggestions = [s for s in suggestions if s['block']]
    non_blocking_suggestions = [s for s in suggestions if not s['block']]

    if blocking_suggestions:
        print("\n🛑 建議使用更好的替代方案：\n", file=sys.stderr)
        for s in blocking_suggestions:
            print(f"❌ 當前命令：{s['original'][:60]}...", file=sys.stderr)
            print(f"✅ 建議使用：{s['better']}", file=sys.stderr)
            print(f"💡 原因：{s['reason']}\n", file=sys.stderr)
        sys.exit(2)  # 阻止執行

    if non_blocking_suggestions:
        print("\n💡 提示：有更簡單的方式執行此操作：\n", file=sys.stderr)
        for s in non_blocking_suggestions:
            print(f"📝 當前命令：{s['original'][:60]}...", file=sys.stderr)
            print(f"✨ 建議使用：{s['better']}", file=sys.stderr)
            print(f"💡 優點：{s['reason']}\n", file=sys.stderr)
        print("（當前命令仍會執行，但建議下次使用推薦的方式）\n", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
