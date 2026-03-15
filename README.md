# 🤖 AI Skills Monitor

AI技能全流程监控与评估系统 - 自动抓取、分析、评估AI Agent技能，生成日报并通过邮件推送。

## ✨ 功能特性

- **多源数据抓取**: 自动监控GitHub、skills.sh等多个技能源
- **智能评估引擎**: 
  - OpenCode兼容性检测
  - 安全风险评估
  - 使用价值评分
- **自动化报告**: 生成美观的HTML日报
- **邮件推送**: 支持SendGrid和SMTP两种方式
- **零成本部署**: 基于GitHub Actions，完全免费运行

## 📁 项目结构

```
ai-skills-monitor/
├── .github/workflows/       # GitHub Actions配置
│   └── skill-monitor.yml    # 定时任务配置
├── src/                     # 源代码
│   ├── monitor.py          # 主入口
│   ├── fetchers/           # 数据抓取器
│   │   ├── github_fetcher.py
│   │   └── skills_sh_fetcher.py
│   ├── evaluators/         # 评估器
│   │   ├── compatibility_checker.py
│   │   ├── security_scanner.py
│   │   └── value_assessor.py
│   ├── reporters/          # 报告生成器
│   │   ├── email_reporter.py
│   │   └── html_generator.py
│   └── utils/              # 工具模块
│       ├── database.py
│       └── logger.py
├── data/                    # 数据存储
├── reports/                 # 报告输出
├── requirements.txt         # 依赖清单
└── README.md
```

## 🚀 快速部署

### 1. Fork本仓库

点击右上角的"Fork"按钮，将仓库复制到你的GitHub账号下。

### 2. 配置GitHub Secrets

进入仓库的 **Settings -> Secrets and variables -> Actions**，添加以下Secrets：

| Secret Name | 说明 | 获取方式 |
|------------|------|---------|
| `GITHUB_TOKEN` | GitHub API Token | 自动提供,无需设置 |
| `EMAIL_RECIPIENT` | 接收报告的邮箱地址 | 你的邮箱 |
| `SMTP_HOST` | SMTP服务器地址 | 如: smtp.gmail.com |
| `SMTP_PORT` | SMTP端口 | 如: 587 |
| `SMTP_USER` | SMTP用户名 | 邮箱地址 |
| `SMTP_PASSWORD` | SMTP密码或应用专用密码 | 邮箱设置中获取 |
| `SENDGRID_API_KEY` | (可选)SendGrid API Key | sendgrid.com |

### 3. 启用GitHub Actions

进入 **Actions** 标签页，点击绿色按钮启用Actions。

### 4. 手动测试运行

进入 **Actions -> AI Skills Daily Monitor**，点击 **Run workflow** 手动触发一次测试。

## ⚙️ 配置说明

### 监控源配置

编辑 `src/monitor.py` 中的 `MONITORED_REPOS` 列表，添加/删除要监控的仓库：

```python
MONITORED_REPOS = [
    {"owner": "anthropics", "repo": "skills", "name": "Anthropic官方"},
    {"owner": "vercel-labs", "repo": "skills", "name": "Vercel Labs"},
    # 添加你的仓库...
]
```

### 定时任务配置

编辑 `.github/workflows/skill-monitor.yml` 中的 `schedule`：

```yaml
schedule:
  - cron: '0 6,12,18 * * *'  # 每天6点、12点、18点运行(UTC)
```

Cron表达式格式：`分 时 日 月 周`

### 本地运行测试

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/ai-skills-monitor.git
cd ai-skills-monitor

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export GITHUB_TOKEN=your_token
export EMAIL_RECIPIENT=your@email.com
export TEST_MODE=true  # 测试模式,不发送邮件

# 运行监控
python src/monitor.py
```

## 📊 评估维度

### 兼容性评估
- ✅ SKILL.md格式规范
- ✅ 系统工具使用权限
- ✅ 无硬编码凭证
- ✅ Bash命令安全性
- ✅ 结构完整性

### 安全评估
- 🔴 **高风险**: 文件删除、代码注入、硬编码密钥
- 🟡 **中风险**: 文件写入、外部网络调用
- 🟢 **低风险**: 只读操作、安全代码

### 价值评估
- 📚 文档完整性
- 💡 示例丰富度
- 🎯 功能独特性
- 🔧 可维护性

## 📧 邮件报告示例

报告包含：
- 📈 统计数据总览
- ⚠️ 高风险警告
- 🔥 必装推荐
- 📦 可选安装
- 📊 完整技能列表

## 🔒 安全说明

- 所有敏感信息通过GitHub Secrets管理
- 代码中无硬编码凭证
- 支持私有仓库监控
- 数据仅存储在你的GitHub仓库中

## 🤝 贡献指南

欢迎提交Issue和PR！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 💬 联系方式

如有问题或建议，欢迎提交Issue。

---

**Star ⭐ 本项目以支持开发！**
