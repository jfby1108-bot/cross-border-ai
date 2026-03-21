# 产品需求文档 (PRD) - 详细版

**项目**：跨境电商 AI 客服系统  
**版本**：V1.0 MVP（详细版）  
**日期**：2026-03-19  
**产品负责人**：Product Team (Julian + Derek)

---

## 1. 产品概述

### 1.1 目标
为跨境电商卖家提供 24/7 AI 客服，自动回复买家消息，提升响应速度，减少差评。

### 1.2 目标用户
- 年销售额 $50万-$500万 的亚马逊/eBay/Shopify 卖家
- 痛点：无法 24h 响应、小语种客服短缺

### 1.3 核心价值
- ⏱️ **响应效率**：7×24h 实时响应，平均 < 3 秒
- 🌐 **语言覆盖**：消除小语种客服缺口
- 💰 **成本优化**：替代部分人工客服，降低运营成本

---

## 2. 功能详细描述

### 2.1 核心功能模块

#### 2.1.1 AI 自动回复引擎

| 功能点 | 详细描述 | 优先级 |
|--------|----------|--------|
| **智能回复生成** | 基于 GPT-4 生成自然流畅的回复内容 | P0 |
| **回复风格配置** | 支持正式/友好/简洁三种风格可选 | P0 |
| **上下文记忆** | 同一对话上下文内保持连贯性（最多 5 轮） | P1 |
| **敏感词过滤** | 自动过滤/替换违禁词和不当内容 | P0 |
| **回复审核** | 开启时高风险回复需人工确认后发送 | P1 |

#### 2.1.2 多语言支持

| 语言 | 代码 | 场景 |
|------|------|------|
| 英语 | en | 默认，主要市场 |
| 中文（简体） | zh-CN | 中国供应商/买家 |
| 日语 | ja | 日本市场 |
| 韩语 | ko | 韩国市场 |
| 德语 | de | 欧洲市场 |
| 法语 | fr | 欧洲市场 |
| 西班牙语 | es | 拉美/西班牙市场 |

**语言检测**：自动识别来信语言并使用对应语言回复（可配置默认语言）

#### 2.1.3 意图识别模块

| 意图类型 | 描述 | 回复策略 |
|----------|------|----------|
| **产品咨询** | 询问产品详情、规格、用途 | 提供详细产品信息 |
| **订单查询** | 物流状态、发货时间、订单修改 | 调用订单 API 查询 |
| **售后问题** | 退货、换货、质量问题 | 触发售后流程 |
| **价格谈判** | 讨价还价、折扣请求 | 根据策略回复 |
| **投诉抱怨** | 不满、差评威胁 | 转人工处理 |
| **闲聊** | 问候、闲聊 | 友好简短回应 |

**准确率目标**：> 85%（可通过反馈持续优化）

#### 2.1.4 常见问题知识库

| 功能 | 描述 |
|------|------|
| **FAQ 导入** | 支持 CSV/JSON 格式批量导入 |
| **关键词匹配** | 快速匹配标准答案 |
| **答案版本管理** | 支持多版本答案 |
| **分类管理** | 按产品/场景/渠道分类 |

#### 2.1.5 人工接管流程

| 触发条件 | 处理方式 |
|----------|----------|
| 买家明确要求人工 | 立即转接 |
| 识别为投诉意图 | 标记并转接 |
| AI 置信度 < 60% | 建议转人工 |
| 连续 3 次未解决 | 自动转人工 |

**人工接管功能**：
- 客服接管后显示完整对话历史
- 支持切换 AI / 人工模式
- 接管记录可追溯

### 2.2 接入渠道

#### 2.2.1 Email 邮件渠道（P0）

| 功能 | 描述 |
|------|------|
| **IMAP 收信** | 定时拉取新邮件 |
| **SMTP 发信** | AI 回复发送邮件 |
| **邮件解析** | 提取 subject、body、from、attachments |
| **邮件模板** | 支持自定义回复模板 |

#### 2.2.2 Amazon 消息渠道（P1）

| 功能 | 描述 |
|------|------|
| **Amazon API 集成** | 通过 Selling Partner API 接收消息 |
| **消息推送** | 新消息实时推送到系统 |
| **回复同步** | 回复同步到 Amazon 买家消息 |

#### 2.2.3 WhatsApp 商业渠道（P2）

| 功能 | 描述 |
|------|------|
| **WhatsApp Business API** | 接入 Meta WhatsApp Business |
| **消息接收** | 接收买家消息 |
| **模板消息** | 支持 WhatsApp 模板消息 |

---

## 3. 用户流程

### 3.1 买家咨询流程（Email 为例）

```
┌──────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ 买家发邮件 │───▶│ 系统收邮件  │───▶│ 意图识别引擎 │───▶│ 决策路由    │
└──────────┘    └─────────────┘    └──────────────┘    └─────────────┘
                                                                     │
                    ┌───────────────────────────────────────────────┘
                    ▼
         ┌──────────────────┐
         │ 置信度判断       │
         └──────────────────┘
            │            │
       >= 60%          < 60%
            │            │
            ▼            ▼
   ┌────────────┐   ┌────────────┐
   │ 知识库匹配  │   │ 转人工队列  │
   └────────────┘   └────────────┘
        │              │
        ▼              ▼
   ┌────────────┐   ┌────────────┐
   │ 生成回复   │   │ 通知客服   │
   └────────────┘   └────────────┘
        │
        ▼
   ┌────────────┐   ┌────────────┐
   │ 审核检查   │──▶│ 发送邮件   │
   └────────────┘   └────────────┘
```

### 3.2 卖家配置流程

```
┌──────────────┐
│  卖家登录    │
└──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  渠道配置    │───▶│  API Key 配置 │
└──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  语言设置    │───▶│  默认语言    │
└──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  回复风格    │───▶│  正式/友好   │
└──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  FAQ 导入    │───▶│  知识库初始化 │
└──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐
│  启用服务    │
└──────────────┘
```

### 3.3 人工接管流程

```
┌──────────────┐
│  触发转人工  │
└──────────────┘
       │
       ▼
┌──────────────┐
│  通知客服    │
│ (邮件/站内)  │
└──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  客服登录    │───▶│  查看对话    │
└──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│  人工回复    │───▶│  结束对话    │
└──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐
│  记录归档    │
└──────────────┘
```

---

## 4. API 接口清单

### 4.1 对外接口（面向卖家/前端）

#### 4.1.1 认证模块

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 注册 | POST | /api/v1/auth/register | 卖家注册账号 |
| 登录 | POST | /api/v1/auth/login | 获取 JWT Token |
| 刷新 Token | POST | /api/v1/auth/refresh | 刷新访问令牌 |
| 登出 | POST | /api/v1/auth/logout | 退出登录 |

#### 4.1.2 渠道配置

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 渠道列表 | GET | /api/v1/channels | 获取已配置渠道 |
| 添加渠道 | POST | /api/v1/channels | 添加新渠道 |
| 更新渠道 | PUT | /api/v1/channels/{id} | 更新渠道配置 |
| 删除渠道 | DELETE | /api/v1/channels/{id} | 删除渠道 |
| 测试连接 | POST | /api/v1/channels/{id}/test | 测试渠道连接 |

#### 4.1.3 AI 配置

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 获取配置 | GET | /api/v1/ai/config | 获取 AI 回复配置 |
| 更新配置 | PUT | /api/v1/ai/config | 更新 AI 回复配置 |
| 回复风格 | PUT | /api/v1/ai/style | 设置回复风格 |

#### 4.1.4 知识库管理

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| FAQ 列表 | GET | /api/v1/knowledge/faqs | 获取 FAQ 列表 |
| 添加 FAQ | POST | /api/v1/knowledge/faqs | 添加单条 FAQ |
| 批量导入 | POST | /api/v1/knowledge/faqs/import | 批量导入 FAQ |
| 更新 FAQ | PUT | /api/v1/knowledge/faqs/{id} | 更新 FAQ |
| 删除 FAQ | DELETE | /api/v1/knowledge/faqs/{id} | 删除 FAQ |
| 搜索 | GET | /api/v1/knowledge/search | 搜索知识库 |

#### 4.1.5 对话管理

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 对话列表 | GET | /api/v1/conversations | 获取对话列表 |
| 对话详情 | GET | /api/v1/conversations/{id} | 获取对话详情 |
| 转人工 | POST | /api/v1/conversations/{id}/transfer | 转接人工 |
| 人工回复 | POST | /api/v1/conversations/{id}/reply | 人工发送回复 |
| 结束对话 | POST | /api/v1/conversations/{id}/close | 结束对话 |

#### 4.1.6 统计报表

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 仪表盘 | GET | /api/v1/stats/dashboard | 获取统计数据 |
| 对话统计 | GET | /api/v1/stats/conversations | 对话统计数据 |
| 响应时间 | GET | /api/v1/stats/response-time | 响应时间统计 |
| 意图分布 | GET | /api/v1/stats/intents | 意图识别统计 |

#### 4.1.7 Webhook 回调

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 注册 Webhook | POST | /api/v1/webhooks | 注册回调地址 |
| Webhook 列表 | GET | /api/v1/webhooks | 获取 Webhook 列表 |
| 删除 Webhook | DELETE | /api/v1/webhooks/{id} | 删除 Webhook |

### 4.2 内部接口（消息处理）

| 接口 | 方法 | 路径 | 描述 |
|------|------|------|------|
| 处理邮件 | POST | /api/internal/email/process | 处理收到的邮件 |
| 意图识别 | POST | /api/internal/ai/classify | 意图分类 |
| 生成回复 | POST | /api/internal/ai/generate | 生成 AI 回复 |
| 发送邮件 | POST | /api/internal/email/send | 发送回复邮件 |

---

## 5. 技术需求

### 5.1 技术栈

| 层级 | 技术选型 |
|------|----------|
| **后端框架** | Python FastAPI |
| **AI 能力** | OpenAI GPT-4 / GPT-4o |
| **数据库** | PostgreSQL + Redis |
| **消息队列** | RabbitMQ / Redis Queue |
| **部署** | Docker + Kubernetes |
| **日志** | ELK Stack |

### 5.2 数据模型

#### 5.2.1 卖家账户 (Seller)
```
- id: UUID
- email: string (unique)
- password_hash: string
- company_name: string
- plan: enum (free, pro)
- created_at: datetime
- updated_at: datetime
```

#### 5.2.2 渠道配置 (Channel)
```
- id: UUID
- seller_id: UUID (FK)
- type: enum (email, amazon, whatsapp)
- config: JSON (IMAP/SMTP keys, API credentials)
- status: enum (active, inactive, error)
- created_at: datetime
```

#### 5.2.3 FAQ 知识库 (KnowledgeBase)
```
- id: UUID
- seller_id: UUID (FK)
- question: text
- answer: text
- language: string
- category: string
- keywords: array
- version: int
- is_active: boolean
- created_at: datetime
- updated_at: datetime
```

#### 5.2.4 对话记录 (Conversation)
```
- id: UUID
- seller_id: UUID (FK)
- channel_id: UUID (FK)
- customer_id: string
- customer_email: string
- status: enum (active, ai_replying, waiting_human, resolved)
- language: string
- started_at: datetime
- ended_at: datetime
```

#### 5.2.5 消息记录 (Message)
```
- id: UUID
- conversation_id: UUID (FK)
- direction: enum (inbound, outbound)
- content: text
- intent: string (resolved_by_ai, human, faq_match)
- confidence: float
- is_approved: boolean (for AI messages needing review)
- created_at: datetime
```

### 5.3 性能要求

| 指标 | 要求 |
|------|------|
| API 响应时间 | P95 < 200ms |
| AI 生成响应 | < 3 秒 |
| 系统可用性 | 99.9% |
| 并发支持 | 1000 QPS |

### 5.4 安全要求

| 要求 | 描述 |
|------|------|
| **数据传输** | 全链路 HTTPS |
| **数据存储** | 敏感数据 AES-256 加密 |
| **API 认证** | JWT Token + API Key |
| **访问控制** | RBAC 权限模型 |
| **审计日志** | 记录所有敏感操作 |
| **数据隔离** | 多租户数据隔离 |

### 5.5 第三方集成

| 服务商 | 用途 | 接入方式 |
|--------|------|----------|
| OpenAI | GPT-4 AI 能力 | API |
| Amazon SP API | Amazon 消息 | API |
| Meta WhatsApp | WhatsApp Business | Business API |
| SendGrid / SES | 邮件发送 | SMTP/API |
| AWS S3 | 文件存储 | SDK |

---

## 6. 定价策略（详细版）

| 功能 | 免费版 | 专业版 ($99/月) |
|------|--------|-----------------|
| 消息额度 | 50 条/月 | 无限 |
| 渠道数量 | 1 | 无限 |
| 语言支持 | 3 种 | 全部 7 种 |
| FAQ 容量 | 50 条 | 无限 |
| 人工接管 | 不支持 | 支持 |
| 统计报表 | 基础 | 高级 |
| API 访问 | 不支持 | 支持 |
| 优先级支持 | 社区 | 邮件+工单 |

---

## 7. 开发里程碑

| 阶段 | 周次 | 交付物 | 验收标准 |
|------|------|--------|----------|
| **Sprint 1** | 1-2 | 项目初始化 + 基础架构 | 代码可运行，CI/CD 就绪 |
| **Sprint 2** | 2-3 | Email 接入 + 基础 AI 回复 | 能收邮件并自动回复 |
| **Sprint 3** | 3-4 | 意图识别 + FAQ 知识库 | 意图识别率 > 80% |
| **Sprint 4** | 4-5 | 多语言支持 + 人工接管 | 7 种语言可用 |
| **Sprint 5** | 5-6 | 卖家后台 + 统计功能 | 可配置可查看数据 |
| **Sprint 6** | 6-7 | 内部测试 + Bug 修复 | 无阻断 Bug |
| **Sprint 7** | 7-8 | UAT + 上线准备 | 通过验收 |

---

## 8. 风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| GPT API 成本超支 | 高 | 设置用量上限预警 |
| Amazon API 变更 | 中 | 模块化接入，保持 API 版本控制 |
| 意图识别准确率不足 | 高 | 持续收集标注数据优化模型 |
| 数据合规 (GDPR/CCPA) | 高 | 数据脱敏 + 用户同意机制 |
| 邮件投递进垃圾箱 | 中 | 邮件认证 (SPF/DKIM/DMARC) |

---

## 9. 附录

### 9.1 术语表

| 术语 | 定义 |
|------|------|
| Intent | 买家消息的意图/目的 |
| FAQ | 常见问题解答 |
| IMAP | 邮件接收协议 |
| SMTP | 邮件发送协议 |
| RBAC | 基于角色的访问控制 |

### 9.2 参考文档

- Amazon Selling Partner API: https://developer.amazonservices.com/
- OpenAI API: https://platform.openai.com/docs
- WhatsApp Business API: https://developers.facebook.com/docs/whatsapp

---

**文档状态**：Ready for Development  
**下一步**：移交开发团队 (Jordan + Ethan) 实现 V1.0
