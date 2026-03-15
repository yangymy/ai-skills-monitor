# AI Skills Monitor - 自动修复脚本
# 用法: 将此脚本内容复制到GitHub网页执行

## 步骤1: 创建缺失的目录结构

在GitHub网页上，点击 "Add file" → "Create new file"

### 1.1 创建工作流文件
文件名: `.github/workflows/skill-monitor.yml`

内容:
```yaml
name: AI Skills Daily Monitor

on:
  schedule:
    - cron: '0 6,12,18 * * *'
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      - run: pip install -r requirements.txt
      - run: python src/monitor.py
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          EMAIL_RECIPIENT: ${{ secrets.EMAIL_RECIPIENT }}
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
          TEST_MODE: false
      - uses: actions/upload-artifact@v4
        with:
          name: daily-report
          path: reports/
          retention-days: 30
```

### 1.2 提交文件
- 点击 "Commit new file"

---

## 步骤2: 配置Secrets

访问: https://github.com/yangymy/ai-skills-monitor/settings/secrets/actions

添加以下5个Secret:

1. EMAIL_RECIPIENT = 873974555@qq.com
2. SMTP_HOST = smtp.qq.com
3. SMTP_PORT = 587
4. SMTP_USER = 873974555@qq.com
5. SMTP_PASSWORD = [你的QQ邮箱授权码]

---

## 步骤3: 启用Actions

访问: https://github.com/yangymy/ai-skills-monitor/actions

点击 "I understand my workflows, go ahead and enable them"

---

## 完成！

系统将在每天6点、12点、18点自动运行，并发送报告到你的邮箱。
