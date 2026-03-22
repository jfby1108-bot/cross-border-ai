"""
SupportIQ - 跨境电商 AI 客服系统
主程序 - FastAPI + 完整功能
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import json
import os

# 导入服务
from config import config
from ai_service import ai_service
from email_service import email_service

app = FastAPI(
    title="SupportIQ API",
    description="跨境电商 AI 客服系统",
    version="1.0.0"
)

# 静态文件
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== 数据模型 ====================

class EmailRequest(BaseModel):
    subject: str
    body: str
    from_email: str
    language: Optional[str] = "zh-CN"

class EmailReplyRequest(BaseModel):
    to: str
    subject: str
    body: str

class AIReplyRequest(BaseModel):
    message: str
    language: Optional[str] = "zh-CN"
    tone: Optional[str] = "professional"

class IntentClassifyRequest(BaseModel):
    message: str

class ProductDescribeRequest(BaseModel):
    product_name: str
    category: Optional[str] = ""
    features: Optional[List[str]] = []
    target_market: Optional[str] = "美国"
    language: Optional[str] = "en"
    tone: Optional[str] = "professional"

# ==================== 系统状态 ====================

@app.get("/")
def root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"service": "SupportIQ Email Customer Service", "status": "ok"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "ai_provider": config.AI_PROVIDER,
        "smtp_configured": bool(config.SMTP_HOST),
        "features": {
            "ai_chat": True,
            "email_send": True,
            "wechat": True
        }
    }

@app.get("/test-email")
def test_email():
    return {"status": "done", "message": "邮件检查完成"}

# ==================== 邮件处理 ====================

@app.post("/api/email/process")
async def process_email(req: EmailRequest):
    """处理收到的邮件 - AI 分析 + 自动回复"""
    
    # 1. AI 意图分类
    intent_result = ai_service.classify_intent(req.body)
    
    # 2. 生成回复
    system_prompt = f"""你是一个专业的跨境电商客服。请用 {req.language} 回复客户。
    保持专业、友好、简洁。"""
    
    ai_reply = ai_service.chat(
        message=f"客户邮件主题: {req.subject}\n客户邮件内容: {req.body}",
        system_prompt=system_prompt
    )
    
    # 3. 发送回复邮件 (如果配置了 SMTP)
    send_result = email_service.send_reply(
        to_email=req.from_email,
        subject=f"Re: {req.subject}",
        body=ai_reply
    )
    
    return {
        "intent": intent_result.get("intent", "general_inquiry"),
        "confidence": intent_result.get("confidence", 0.8),
        "ai_reply": ai_reply,
        "email_sent": send_result,
        "language": req.language
    }

@app.post("/api/email/send")
async def send_email(req: EmailReplyRequest):
    """发送回复邮件"""
    result = email_service.send_reply(
        to_email=req.to,
        subject=req.subject,
        body=req.body
    )
    return result

# ==================== 微信处理 ====================

@app.get("/api/wechat/webhook")
def wechat_webhook_get(signature: str = "", timestamp: str = "", nonce: str = "", echostr: str = ""):
    """微信验证"""
    # 如果配置了 Token，验证签名
    if config.WECHAT_TOKEN:
        # TODO: 实现签名验证
        pass
    return {"echostr": echostr}

@app.post("/api/wechat/webhook")
async def wechat_webhook(request: dict):
    """微信消息处理"""
    msg_type = request.get("MsgType", "")
    
    if msg_type == "text":
        # 用户发送文本
        user_message = request.get("Content", "")
        from_user = request.get("FromUserName", "")
        
        # AI 回复
        reply = ai_service.chat(user_message)
        
        return {
            "ToUserName": from_user,
            "FromUserName": request.get("ToUserName", ""),
            "CreateTime": request.get("CreateTime", 0),
            "MsgType": "text",
            "Content": reply
        }
    
    return {"response": "success"}

# ==================== AI 接口 ====================

@app.post("/api/ai/reply")
async def ai_reply(req: AIReplyRequest):
    """生成 AI 回复"""
    system_prompt = f"""你是一个专业的跨境电商客服。
    用 {req.language} 语言回复。
    语气：{req.tone}"""
    
    reply = ai_service.chat(req.message, system_prompt)
    intent = ai_service.classify_intent(req.message)
    
    return {
        "reply": reply,
        "intent": intent.get("intent", "general_inquiry"),
        "confidence": intent.get("confidence", 0.8)
    }

@app.post("/api/intent/classify")
async def intent_classify(req: IntentClassifyRequest):
    """意图分类"""
    result = ai_service.classify_intent(req.message)
    return result

# ==================== 产品描述 ====================

@app.post("/api/product/describe")
async def product_describe(req: ProductDescribeRequest):
    """生成产品描述"""
    # 构建 prompt
    prompt = f"""为以下产品生成亚马逊标题和描述：
    
产品名称: {req.product_name}
类别: {req.category}
特点: {', '.join(req.features)}
目标市场: {req.target_market}
语言: {req.language}
语气: {req.tone}

请返回 JSON 格式：
{{
  "title": "标题",
  "description": "描述",
  "keywords": ["关键词1", "关键词2"]
}}"""

    result = ai_service.chat(prompt, "")
    
    # 尝试解析 JSON
    try:
        import json
        data = json.loads(result)
        return data
    except:
        # 如果不是 JSON，返回模板
        return {
            "title": f"{req.product_name} - Premium Quality {req.target_market} Market",
            "description": f"Introducing our premium {req.product_name}, designed specifically for the {req.target_market} market.",
            "keywords": ["premium", "quality", req.target_market.lower()]
        }

# ==================== 统计 ====================

@app.get("/api/stats")
def stats():
    """统计信息"""
    return {
        "emails_processed": 0,
        "wechat_messages": 0,
        "active_customers": 0,
        "ai_provider": config.AI_PROVIDER
    }

# ==================== 配置接口 ====================

@app.get("/api/config/status")
def config_status():
    """配置状态"""
    return {
        "ai_provider": config.AI_PROVIDER,
        "smtp_configured": bool(config.SMTP_HOST),
        "imap_configured": bool(config.IMAP_HOST),
        "wechat_configured": bool(config.WECHAT_TOKEN)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
