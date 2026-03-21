# 微信自动回复 MVP (简化版)
# 仅实现：关键词自动回复 + 消息转发

import os
import json
import time
import hashlib
import threading
from datetime import datetime
from typing import Dict, Optional
from flask import Flask, request, jsonify
from dataclasses import dataclass

# ============ 配置 ============

CONFIG = {
    "wechat_token": os.getenv("WECHAT_TOKEN", "your-secret-token"),
    "wechat_appid": os.getenv("WECHAT_APPID", ""),
    "wechat_secret": os.getenv("WECHAT_SECRET", ""),
    "ai_model": os.getenv("AI_MODEL", "qwen"),
    "ai_api_key": os.getenv("AI_API_KEY", ""),
    "forward_to_wechat": os.getenv("FORWARD_TO_WECHAT", ""),  # 转发到的微信号
}

# 关键词回复表
KEYWORD_REPLIES = {
    # 产品相关
    "产品": "感谢您的咨询！我们的 AI 客服系统支持多平台（亚马逊/eBay/Shopify），提供 24/7 自动回复。如需了解详情，请回复「价格」或「功能」。",
    "价格": "💰 价格方案：\n- 基础版：$99/月（1000条消息）\n- 专业版：$199/月（5000条消息）\n- 企业版：$399/月（无限消息）\n\n回复「1」了解基础版、「2」了解专业版、「3」了解企业版",
    "功能": "🔧 核心功能：\n- AI 自动回复（支持 7+ 语言）\n- 智能意图识别\n- FAQ 知识库\n- 人工接管无缝切换\n- 多平台统一管理\n\n如需演示，请留下您的联系方式",
    
    # 常见问题
    "物流": "📦 物流查询：请提供您的订单号，我来帮您查询物流状态",
    "发货": "📦 发货时间：订单确认后 1-2 个工作日内发货，快递时效 3-7 天",
    "退货": "🔄 退货政策：7 天无理由退货，请联系客服获取退货地址",
    "退款": "💳 退款说明：退货收到后 3-5 个工作日内退款到原支付方式",
    
    # 问候
    "你好": "👋 您好！我是 AI 客服，有什么可以帮您？",
    "hello": "👋 Hello! How can I help you today?",
    "hi": "👋 Hi there! Feel free to ask me anything.",
    
    # 默认
    "default": "感谢您的留言！我们的工作时间 9:00-18:00（周一至周五）。如需人工服务，请回复「人工」。我会尽快回复您！"
}

# 意图模板
INTENT_TEMPLATES = {
    "order_inquiry": {
        "keywords": ["订单", "order", "物流", "shipping", "快递", "到了吗"],
        "reply": "📦 请提供您的订单号，我来帮您查询物流状态"
    },
    "refund_request": {
        "keywords": ["退款", "退货", "refund", "return", "不要了"],
        "reply": "🔄 抱歉给您带来不便。请问是因为质量问题还是其他原因？我们可以提供换货或退款服务。"
    },
    "product_question": {
        "keywords": ["产品", "product", "规格", "spec", "参数"],
        "reply": "📝 请问您想了解哪款产品的具体信息？您可以告诉我产品名称或类别。"
    },
    "price_inquiry": {
        "keywords": ["价格", "price", "多少钱", "cost", "报价"],
        "reply": "💰 您想了解哪款产品的价格？我可以为您发送详细的价格表。"
    },
    "complaint": {
        "keywords": ["投诉", "complaint", "不满", "差评", "体验差"],
        "reply": "😔 非常抱歉给您带来不好的体验。请您详细描述问题，我会立即转交专人处理。"
    },
    "human_agent": {
        "keywords": ["人工", "客服", "真人", "human", "人工服务"],
        "reply": "👤 好的，我将为您转接人工客服。请稍候..."
    }
}

# ============ 数据模型 ============

@dataclass
class WechatMessage:
    msg_id: str
    from_user: str
    msg_type: str
    content: str
    create_time: int

# ============ 消息处理 ============

def classify_intent(content: str) -> str:
    """意图分类"""
    content_lower = content.lower()
    
    for intent, template in INTENT_TEMPLATES.items():
        for keyword in template["keywords"]:
            if keyword.lower() in content_lower:
                return intent
    
    return "default"

def get_reply(content: str) -> str:
    """获取回复内容"""
    content_lower = content.lower()
    
    # 1. 精确匹配关键词
    for keyword, reply in KEYWORD_REPLIES.items():
        if keyword.lower() in content_lower:
            return reply
    
    # 2. 意图匹配
    intent = classify_intent(content)
    if intent in INTENT_TEMPLATES:
        return INTENT_TEMPLATES[intent]["reply"]
    
    # 3. 默认回复
    return KEYWORD_REPLIES["default"]

def handle_text_message(msg: WechatMessage) -> str:
    """处理文本消息"""
    content = msg.content.strip()
    
    # 简单 AI 增强版（生产环境可接入 GPT/Qwen）
    # 这里先用规则 + 模板
    
    reply = get_reply(content)
    
    # 如果需要转人工
    if "人工" in content or "human" in content.lower():
        # TODO: 触发人工接管流程
        print(f"⚠️ 用户请求人工: {msg.from_user}")
    
    return reply

def handle_event_message(msg: WechatMessage) -> str:
    """处理事件消息"""
    # 关注/取消关注事件
    if msg.content == "subscribe":
        return "👋 欢迎关注！我们是 SupportIQ，专注跨境电商 AI 客服。如需帮助，请随时留言。"
    elif msg.content == "unsubscribe":
        print(f"用户取消关注: {msg.from_user}")
        return ""
    
    return ""

# ============ Flask API ============

app = Flask(__name__)

@app.route("/wechat", methods=["GET", "POST"])
def wechat_endpoint():
    """微信服务器验证 + 消息接收"""
    
    # GET 请求：验证服务器
    if request.method == "GET":
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")
        
        # 验证签名
        token = CONFIG["wechat_token"]
        tmp_list = sorted([token, timestamp, nonce])
        tmp_str = "".join(tmp_list)
        hash_str = hashlib.sha1(tmp_str.encode()).hexdigest()
        
        if hash_str == signature:
            return echostr
        else:
            return "signature error", 403
    
    # POST 请求：处理消息
    try:
        xml_data = request.data.decode("utf-8")
        import xml.etree.ElementTree as ET
        
        root = ET.fromstring(xml_data)
        msg_type = root.find("MsgType").text
        from_user = root.find("FromUserName").text
        msg_id = root.find("MsgId").text
        create_time = int(root.find("CreateTime").text or "0")
        
        if msg_type == "text":
            content = root.find("Content").text or ""
            msg = WechatMessage(msg_id, from_user, msg_type, content, create_time)
            reply_content = handle_text_message(msg)
            
        elif msg_type == "event":
            event = root.find("Event").text or ""
            msg = WechatMessage(msg_id, from_user, msg_type, event, create_time)
            reply_content = handle_event_message(msg)
            
        else:
            reply_content = "不支持的消息类型"
        
        # 生成回复 XML
        to_user = from_user
        from_user = "your_wechat_id"  # 公众号 ID
        
        reply_xml = f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{reply_content}]]></Content>
</xml>"""
        
        return reply_xml
        
    except Exception as e:
        print(f"处理消息失败: {e}")
        return "success", 200

@app.route("/health")
def health():
    """健康检查"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

# ============ 主程序 ============

if __name__ == "__main__":
    import sys
    
    port = int(os.getenv("PORT", "5000"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 测试意图分类
        test_messages = [
            "我的订单什么时候到",
            "我想退货",
            "产品怎么卖",
            "你们有客服吗",
            "hello"
        ]
        
        print("🧪 意图分类测试\n")
        for msg in test_messages:
            intent = classify_intent(msg)
            reply = get_reply(msg)
            print(f"输入: {msg}")
            print(f"意图: {intent}")
            print(f"回复: {reply}")
            print("-" * 40)
            
    else:
        print(f"🚀 微信自动回复服务启动 (端口 {port})")
        print(f"Token: {CONFIG['wechat_token'][:10]}...")
        app.run(host="0.0.0.0", port=port, debug=True)