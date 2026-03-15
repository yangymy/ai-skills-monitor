# AI技能监控系统 - 部署指南

## 🎯 部署步骤（5分钟内完成）

### 步骤1: 创建GitHub仓库

1. 访问 https://github.com/new
2. 仓库名称填写: `ai-skills-monitor`
3. 选择 "Public" 或 "Private"
4. 勾选 "Add a README file"
5. 点击 "Create repository"

### 步骤2: 上传代码

在本地执行：

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/ai-skills-monitor.git
cd ai-skills-monitor

# 创建目录结构
mkdir -p .github/workflows src/{fetchers,evaluators,reporters,utils} data reports

# 复制所有代码文件到对应目录
# ... (将上面生成的所有文件放入对应位置)

# 提交代码
git add .
git commit -m "Initial commit: AI Skills Monitor"
git push origin main
```

### 步骤3: 配置Secrets

1. 进入仓库页面
2. 点击 **Settings** 标签
3. 左侧菜单选择 **Secrets and variables -> Actions**
4. 点击 **New repository secret** 逐个添加：

#### 必需配置：

| Secret名称 | 值 | 说明 |
|-----------|-----|------|
| `EMAIL_RECIPIENT` | your-email@example.com | 接收报告的邮箱 |

#### SMTP配置（二选一）：

**Gmail用户：**
- `SMTP_HOST`: `smtp.gmail.com`
- `SMTP_PORT`: `587`
- `SMTP_USER`: 你的Gmail地址
- `SMTP_PASSWORD`: [应用专用密码](https://myaccount.google.com/apppasswords)

**其他邮箱：**
- `SMTP_HOST`: 你的SMTP服务器
- `SMTP_PORT`: 你的SMTP端口
- `SMTP_USER`: 邮箱地址
- `SMTP_PASSWORD`: 邮箱密码

#### SendGrid配置（推荐）：

- `SENDGRID_API_KEY`: 从 [SendGrid](https://sendgrid.com/) 获取的API Key

### 步骤4: 启用Actions

1. 点击仓库的 **Actions** 标签
2. 点击 **"I understand my workflows, go ahead and enable them"**
3. 系统会自动开始运行

### 步骤5: 测试运行

1. 进入 **Actions -> AI Skills Daily Monitor**
2. 点击右侧的 **Run workflow** 按钮
3. 等待运行完成(约2-3分钟)
4. 检查邮箱是否收到报告

## 📋 邮件配置详解

### Gmail配置步骤

1. 访问 https://myaccount.google.com/security
2. 开启 "两步验证"
3. 访问 https://myaccount.google.com/apppasswords
4. 选择 "邮件" -> "其他(自定义名称)"
5. 名称填写 "AI Skills Monitor"
6. 复制生成的16位密码
7. 在GitHub Secrets中设置 `SMTP_PASSWORD` 为这个密码

### SendGrid配置步骤（推荐，更稳定）

1. 注册 [SendGrid](https://signup.sendgrid.com/) 账号
2. 完成邮箱验证
3. 创建API Key：
   - Settings -> API Keys -> Create API Key
   - 名称: `AI-Skills-Monitor`
   - 权限: `Restricted Access` -> `Mail Send` -> `Full Access`
4. 复制API Key
5. 在GitHub Secrets中设置 `SENDGRID_API_KEY`
6. 设置 `SMTP_USER` 为你在SendGrid验证过的发件邮箱

## 🔧 高级配置

### 自定义监控源

编辑 `src/monitor.py`：

```python
MONITORED_REPOS = [
    {"owner": "anthropics", "repo": "skills", "name": "Anthropic官方"},
    {"owner": "vercel-labs", "repo": "skills", "name": "Vercel Labs"},
    # 添加你自己的技能仓库
    {"owner": "YOUR_USERNAME", "repo": "YOUR_SKILLS_REPO", "name": "我的技能"},
]
```

### 调整运行频率

编辑 `.github/workflows/skill-monitor.yml`：

```yaml
schedule:
  # 每小时运行一次
  - cron: '0 * * * *'
  
  # 或者每天上午9点运行
  - cron: '0 9 * * *'
```

### 多接收人配置

在 `EMAIL_RECIPIENT` 中填写多个邮箱，用逗号分隔：

```
team1@company.com,team2@company.com,manager@company.com
```

## 🐛 故障排查

### 问题1: 邮件未收到

**检查清单：**
- [ ] SMTP配置正确
- [ ] 邮箱密码是应用专用密码(Gmail)
- [ ] 邮箱地址格式正确
- [ ] 检查垃圾邮件文件夹

**调试方法：**

在Actions日志中查看错误信息：
1. 进入Actions运行记录
2. 点击 "Run skill monitor"
3. 查看日志输出

### 问题2: GitHub API限制

如果遇到API限制：
- 确保设置了 `GITHUB_TOKEN`
- 降低运行频率（不要每小时运行太多次）

### 问题3: 报告为空

可能原因：
- 监控的仓库最近24小时内无更新
- 仓库访问权限问题
- 技能格式不符合规范

## 📞 获取帮助

如有问题：
1. 查看Actions运行日志
2. 提交Issue到本仓库
3. 检查 [GitHub Actions文档](https://docs.github.com/en/actions)

## ✅ 部署检查清单

- [ ] 仓库已创建
- [ ] 所有代码文件已上传
- [ ] GitHub Secrets已配置
- [ ] Actions已启用
- [ ] 手动测试运行成功
- [ ] 收到测试邮件报告

---

**部署完成！** 系统现在会自动每天运行并发送报告到你的邮箱。
