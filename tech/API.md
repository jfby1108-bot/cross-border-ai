# API 接口文档

**版本**：V1.0  
**日期**：2026-03-21

---

## 📡 内部 API

### 1. 邮件处理

#### POST /api/internal/email/process
处理收到的邮件

**请求**：
```json
{
  "subject": "邮件主题",
  "body": "邮件正文",
  "from": "发件人邮箱"
}
```

**响应**：
```json
{
  "intent": "order_inquiry",
  "reply": "AI 生成的回复",
  "confidence": 0.85
}
```

---

#### POST /api/internal/email/send
发送回复邮件

**请求**：
```json
{
  "to": "收件人邮箱",
  "subject": "回复主题",
  "body": "回复内容"
}
```

**响应**：
```json
{
  "success": true,
  "message_id": "xxx"
}
```

---

### 2. 微信处理

#### GET/POST /api/internal/wechat/webhook
微信服务器回调

**参数**：
- signature: 签名
- timestamp: 时间戳
- nonce: 随机数
- echostr: 验证字符串

---

### 3. AI 接口

#### POST /api/internal/ai/reply
生成 AI 回复

**请求**：
```json
{
  "message": "用户消息",
  "language": "zh-CN",
  "tone": "professional"
}
```

**响应**：
```json
{
  "reply": "AI 回复内容",
  "intent": "product_question"
}
```

---

#### POST /api/internal/intent/classify
意图分类

**请求**：
```json
{
  "message": "用户消息"
}
```

**响应**：
```json
{
  "intent": "refund_request",
  "confidence": 0.92
}
```

---

### 4. 产品描述

#### POST /api/internal/product/describe
生成产品描述

**请求**：
```json
{
  "product_name": "产品名称",
  "category": "类别",
  "features": ["特点1", "特点2"],
  "target_market": "美国",
  "language": "en",
  "tone": "professional"
}
```

**响应**：
```json
{
  "title": "生成的标题",
  "description": "生成的产品描述",
  "keywords": ["关键词1", "关键词2"]
}
```

---

## 🔐 认证

所有内部 API 需要在 Header 中携带：
```
Authorization: Bearer <api_key>
```

---

*更新：2026-03-21*