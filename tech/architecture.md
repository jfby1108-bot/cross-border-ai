# 技术架构文档

**项目**：跨境电商 AI 客服系统  
**版本**：V1.0  
**日期**：2026-03-21  
**负责人**：Jordan（开发部）

---

## 1. 系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户层 (Clients)                        │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│  Amazon    │  Shopify    │   Email     │   WeChat/WhatsApp │
└──────┬──────┴──────┬──────┴──────┬──────┴────────┬─────────┘
       │             │             │                │
       ▼             ▼             ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                    API 网关层 (Gateway)                       │
│         OpenClaw / Flask / FastAPI 统一入口                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  意图识别   │    │  AI 回复    │    │  知识库     │
│  (NLU)     │    │  (LLM)      │    │  (KB)       │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据层 (Data)                             │
│      PostgreSQL + Redis + 文件存储 (S3/本地)                │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| API 网关 | OpenClaw / Flask | 统一入口，权限管理 |
| AI 引擎 | Qwen / GPT-4 | 回复生成 |
| 意图识别 | 规则 + BERT/向量 | 意图分类 |
| 数据库 | PostgreSQL | 主数据存储 |
| 缓存 | Redis | 会话/计数器 |
| 消息队列 | Redis Queue | 异步任务 |

---

## 2. 核心模块

### 2.1 邮件客服模块

**功能**：
- IMAP 定时拉取未读邮件
- SMTP 自动发送回复
- 意图分类（订单/退货/价格/产品/闲聊）
- AI 回复生成

**技术**：
- Python + imaplib/smtplib
- 定时任务：APScheduler

**文件**：`mvp/AI-Customer-Service/email_service.py`

### 2.2 微信客服模块

**功能**：
- 微信公众平台 API 对接
- 关键词自动回复
- 意图识别 + AI 回复
- 人工接管触发

**技术**：
- Flask + XML 解析
- 关键词匹配 + 意图分类

**文件**：`mvp/AI-Customer-Service/wechat_service.py`

### 2.3 产品描述生成模块

**功能**：
- 多语言产品描述生成
- Amazon/eBay/Shopify 多平台适配
- SEO 关键词优化
- 多种语气风格

**文件**：`mvp/product-description/product_describer.py`

---

## 3. 数据流

### 3.1 邮件处理流程

```
用户发送邮件 → IMAP 拉取 → 邮件解析 → 意图分类 → AI 生成回复 → 审核（如需）→ SMTP 发送
```

### 3.2 微信处理流程

```
用户发送消息 → 微信服务器验证 → XML 解析 → 意图分类 → 获取回复 → XML 响应
```

---

## 4. API 接口

### 4.1 内部接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/internal/email/process` | POST | 处理邮件 |
| `/api/internal/email/send` | POST | 发送邮件 |
| `/api/internal/wechat/webhook` | GET/POST | 微信回调 |
| `/api/internal/ai/reply` | POST | AI 生成回复 |
| `/api/internal/intent/classify` | POST | 意图分类 |

### 4.2 外部接口

| 平台 | 接口 | 说明 |
|------|------|------|
| Gmail/Outlook | IMAP/SMTP | 邮件收发 |
| 微信公众平台 | HTTP API | 消息收发 |
| Amazon Seller API | REST | 订单查询（可选）|
| Shopify API | GraphQL | 订单查询（可选）|

---

## 5. 部署

### 5.1 开发环境

```bash
pip install -r requirements.txt
cp .env.example .env
# 配置环境变量
python email_service.py
```

### 5.2 生产环境

- 服务器：AWS EC2 / GCP / 阿里云
- 容器：Docker + Docker Compose
- 域名：supportiq.com（待注册）

### 5.3 监控

- 健康检查：`/health`
- 日志：Python logging
- 指标：Prometheus（可选）

---

## 6. 安全

- API 密钥环境变量存储
- 微信 Token 验证
- 邮件敏感信息脱敏
- 数据加密传输（HTTPS）

---

## 7. 待完成

- [ ] 技术架构细化
- [ ] OpenClaw 多 Agent 框架
- [ ] 外部 API 集成（Amazon/Shopify）
- [ ] 生产环境部署

---

*更新：2026-03-21*