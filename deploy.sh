#!/bin/bash
# SupportIQ 部署脚本
# 使用: ./deploy.sh [email|wechat|all]

MODE=${1:-all}
ENV_FILE=".env"

echo "🚀 SupportIQ 部署开始..."

# 检查环境变量
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ 缺少 .env 文件"
    echo "请复制 .env.example 为 .env 并填写配置"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖..."
pip install -r mvp/AI-Customer-Service/requirements.txt

# 启动服务
case $MODE in
    email)
        echo "📧 启动邮件服务..."
        python3 mvp/AI-Customer-Service/email_service.py &
        ;;
    wechat)
        echo "💬 启动微信服务..."
        python3 mvp/AI-Customer-Service/wechat_service.py &
        ;;
    all)
        echo "📧 启动邮件服务..."
        python3 mvp/AI-Customer-Service/email_service.py &
        echo "💬 启动微信服务..."
        python3 mvp/AI-Customer-Service/wechat_service.py &
        ;;
    *)
        echo "❌ 未知模式: $MODE"
        echo "使用: ./deploy.sh [email|wechat|all]"
        exit 1
        ;;
esac

echo "✅ 部署完成！"
echo "服务运行中..."