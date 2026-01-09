# Git 提交並推送

自動執行 Git add、commit 和 push 流程。

## 執行步驟

在一次回應中完成以下所有步驟（不要分開執行）：

1. 檢查當前 git 狀態
2. 查看變更內容
3. 將變更加入暫存區
4. 建立有意義的 commit message
5. 推送到遠端 repository

## Commit Message 格式

遵循 Conventional Commits 規範：
- `feat:` 新功能
- `fix:` 錯誤修復
- `docs:` 文檔更新
- `style:` 程式碼格式調整
- `refactor:` 重構
- `test:` 測試相關
- `chore:` 建置工具或輔助工具變動

每個 commit 都加上：
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## 使用範例

```bash
# 自動分析變更並提交
/commit-push

# 指定 commit message
/commit-push "feat: add new detection endpoint"
```

## 注意事項

- 提交前確認不包含敏感資訊
- 不提交 .pt 模型檔案（已在 .gitignore）
- 不提交資料集圖片（已在 .gitignore）
