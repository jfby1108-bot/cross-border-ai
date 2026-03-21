# 部署指南

**版本**：V1.0  
**日期**：2026-03-21

---

## 🚀 快速部署

### 1. 本地运行

```bash
# 克隆项目
git clone <repository-url>
cd cross-border-ai

# 安装依赖
pip install -r mvp/AI-Customer-Service/requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API 密钥

# 启动邮件服务
python mvp/AI-Customer-Service/email_service.py

# 启动微信服务（新终端）
python mvp/AI-Customer-Service/wechat_service.py
```

---

### 2. 服务器部署

#### 选项 A：Railway（推荐）

```bash
# 1. 注册 railway.app
# 2. 连接 GitHub 仓库
# 3. 设置环境变量
# 4. 部署
```

#### 选项 B：Render

```bash
# 1. 注册 render.com
# 2. 连接 GitHub
# 3. 设置 Build Command: pip install -r requirements.txt
# 4. 设置 Start Command: python email_service.py
```

#### 选项 C：VPS (DigitalOcean/Ubuntu)

```bash
# 1. 创建 Droplet
# 2. SSH 登录
# 3. 安装 Python 和依赖
# 4. 使用 systemd 管理服务

sudo cp supportiq-email.service /etc/systemd/system/
sudo systemctl enable supportiq-email
sudo systemctl start supportiq-email
```

---

## 🔧 环境变量

```bash
# 邮件
IMAP_HOST=imap.gmail.com
IMAP_USER=your-email@gmail.com
IMAP_PASSWORD=app-password

# AI
AI_API_KEY=your-api-key

# 微信
WECHAT_TOKEN=your-token
```

---

## ✅ 检查清单

- [ ] API 密钥已配置
- [ ] 邮件服务测试通过
- [ ] 微信服务测试通过
- [ ] 域名已解析（可选）
- [ ] SSL 证书已安装（可选）

---

## 📦 快速部署（新增）

### 1. 配置文件
```bash
cp .env.example .env
# 编辑 .env 填写实际值
```

### 2. 一键部署
```bash
chmod +x deploy.sh
./deploy.sh all  # 启动所有服务
./deploy.sh email  # 仅邮件
./deploy.sh wechat  # 仅微信
```

### 3. Docker 部署（可选）
```bash
docker-compose up -d
```

---

*更新：2026-03-21*