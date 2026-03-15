#!/bin/bash
# 一键部署脚本 - AI Skills Monitor
# 使用方法: 在仓库目录下运行: bash deploy.sh

echo "========================================"
echo "🤖 AI Skills Monitor 一键部署脚本"
echo "========================================"
echo ""

# 检查git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未安装Git"
    echo "请访问 https://git-scm.com/download 下载安装"
    exit 1
fi

echo "✅ Git已安装"

# 检查当前目录
if [ ! -f "src/monitor.py" ]; then
    echo "❌ 错误: 请在ai-skills-monitor项目根目录运行此脚本"
    echo "当前目录: $(pwd)"
    exit 1
fi

echo "✅ 检测到项目文件"
echo ""

# 配置git（如果未配置）
if ! git config --global user.email &> /dev/null; then
    echo "⚙️  配置Git用户邮箱..."
    git config --global user.email "873974555@qq.com"
fi

if ! git config --global user.name &> /dev/null; then
    echo "⚙️  配置Git用户名..."
    git config --global user.name "AI Monitor"
fi

# 初始化git仓库（如果需要）
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
fi

# 添加远程仓库
echo "🔗 配置远程仓库..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/yangymy/ai-skills-monitor.git

# 添加所有文件
echo "📁 添加文件到Git..."
git add .

# 提交
echo "💾 提交代码..."
git commit -m "Initial commit: AI Skills Monitor" || echo "✅ 无变更需要提交"

# 推送到GitHub
echo "📤 推送到GitHub..."
echo ""
echo "⚠️  注意: 如果要求输入用户名密码，请输入:"
echo "   用户名: yangymy"
echo "   密码: 使用GitHub Personal Access Token"
echo ""

git push -u origin main || git push -u origin master

echo ""
echo "========================================"
echo "✅ 代码上传完成!"
echo "========================================"
echo ""
echo "📝 下一步操作:"
echo ""
echo "1. 打开 https://github.com/yangymy/ai-skills-monitor"
echo "2. 点击 '⚙️ 设置' (Settings)"
echo "3. 左侧点击 'Secrets and variables' → 'Actions'"
echo "4. 点击 'New repository secret' 添加以下5个:"
echo ""
echo "   EMAIL_RECIPIENT = 873974555@qq.com"
echo "   SMTP_HOST = smtp.qq.com"
echo "   SMTP_PORT = 587"
echo "   SMTP_USER = 873974555@qq.com"
echo "   SMTP_PASSWORD = ncorpyflyeflbbic"
echo ""
echo "5. 添加完成后，点击 '行动' (Actions) 标签启用"
echo ""
echo "📧 配置完成后，系统会自动运行并发送报告到你的邮箱"
echo ""

read -p "按回车键退出..."
