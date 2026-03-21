# 邮件客服 MVP - 快速启动版
# 包含：IMAP 收信 + SMTP 发信 + AI 回复

import os
import json
import time
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

# 配置
CONFIG = {
    "imap_host": os.getenv("IMAP_HOST", "imap.gmail.com"),
    "imap_user": os.getenv("IMAP_USER", ""),
    "imap_password": os.getenv("IMAP_PASSWORD", ""),
    "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "smtp_user": os.getenv("SMTP_USER", ""),
    "smtp_password": os.getenv("SMTP_PASSWORD", ""),
    "ai_model": os.getenv("AI_MODEL", "qwen"),
    "ai_api_key": os.getenv("AI_API_KEY", ""),
    "ai_endpoint": os.getenv("AI_ENDPOINT", "https://api.qwen.com/v1"),
    "reply_style": os.getenv("REPLY_STYLE", "professional"),  # professional, friendly, concise
    "default_language": os.getenv("DEFAULT_LANGUAGE", "en"),
    "enable_review": os.getenv("ENABLE_REVIEW", "false").lower() == "true",
}

@dataclass
class Email:
    subject: str
    body: str
    from_email: str
    from_name: str
    date: str
    message_id: str

# ============ 邮件接收 (IMAP) ============

def connect_imap():
    """连接 IMAP 服务器"""
    try:
        import imaplib
        mail = imaplib.IMAP4_SSL(CONFIG["imap_host"])
        mail.login(CONFIG["imap_user"], CONFIG["imap_password"])
        return mail
    except Exception as e:
        print(f"IMAP 连接失败: {e}")
        return None

def fetch_unread_emails(mail, folder="inbox", limit=10) -> List[Email]:
    """获取未读邮件"""
    try:
        mail.select(folder)
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            return []
        
        email_ids = messages[0].split()[:limit]
        emails = []
        
        for eid in email_ids:
            _, msg_data = mail.fetch(eid, "(RFC822)")
            for response in msg_data:
                if isinstance(response, tuple):
                    from email.parser import Parser
                    parser = Parser()
                    msg = parser.parsestr(response[1])
                    
                    email = Email(
                        subject=msg.get("Subject", ""),
                        body=msg.get_payload(decode=True).decode("utf-8", errors="ignore") if msg.get_payload() else "",
                        from_email=msg.get("From", ""),
                        from_name=msg.get("From", ""),
                        date=msg.get("Date", ""),
                        message_id=msg.get("Message-ID", "")
                    )
                    emails.append(email)
        return emails
    except Exception as e:
        print(f"获取邮件失败: {e}")
        return []

# ============ 邮件发送 (SMTP) ============

def connect_smtp():
    """连接 SMTP 服务器"""
    try:
        import smtplib
        server = smtplib.SMTP(CONFIG["smtp_host"], CONFIG["smtp_port"])
        server.starttls()
        server.login(CONFIG["smtp_user"], CONFIG["smtp_password"])
        return server
    except Exception as e:
        print(f"SMTP 连接失败: {e}")
        return None

def send_email(smtp, to_email: str, subject: str, body: str):
    """发送回复邮件"""
    try:
        from email.mime.text import MIMEText
        from email.header import Header
        
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = CONFIG["smtp_user"]
        msg["To"] = to_email
        
        smtp.sendmail(CONFIG["smtp_user"], to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"发送邮件失败: {e}")
        return False

# ============ AI 回复生成 ============

def generate_ai_reply(email: Email) -> str:
    """调用 AI 生成回复"""
    # 简化版：使用预设模板 + 基础关键词匹配
    # 生产版：调用 Qwen/GPT API
    
    body_lower = email.body.lower()
    subject_lower = email.subject.lower()
    combined = body_lower + " " + subject_lower
    
    # 意图识别 + 回复模板
    if any(w in combined for w in ["order", "shipping", "delivery", "物流", "发货"]):
        return get_template("order")
    elif any(w in combined for w in ["refund", "return", "退货", "退款"]):
        return get_template("refund")
    elif any(w in combined for w in ["price", "discount", "折扣", "优惠"]):
        return get_template("price")
    elif any(w in combined for w in ["product", "feature", "产品", "规格"]):
        return get_template("product")
    else:
        return get_template("default")

def get_template(intent: str) -> str:
    """获取回复模板"""
    templates = {
        "order": """Dear Customer,

Thank you for contacting us about your order. I'd be happy to help you check the current status.

Your order is currently being processed and will be shipped within 1-2 business days. You will receive a tracking number via email once shipped.

If you have any other questions, please don't hesitate to reach out.

Best regards,
Support Team""",
        
        "refund": """Dear Customer,

Thank you for reaching out regarding your refund request. I understand your concern and want to help resolve this as quickly as possible.

Our team will review your request within 24-48 hours. If approved, the refund will be processed to your original payment method within 5-7 business days.

Please provide your order number if you haven't already, and we'll expedite this process for you.

Best regards,
Support Team""",
        
        "price": """Dear Customer,

Thank you for your interest in our products. We appreciate your inquiry about pricing.

We're happy to offer a 10% discount on your first order as a new customer. Please use code: WELCOME10 at checkout.

Would you like me to provide more details about our product range?

Best regards,
Support Team""",
        
        "product": """Dear Customer,

Thank you for your inquiry about our products. I'd be happy to provide you with more information.

Could you please let me know which specific product you're interested in? I'd be glad to share detailed specifications, pricing, and availability.

You can also visit our website for the complete catalog.

Best regards,
Support Team""",
        
        "default": """Dear Customer,

Thank you for contacting us. I've received your message and will respond within 24 hours.

If your matter is urgent, please let us know and we'll prioritize your request.

Best regards,
Support Team"""
    }
    return templates.get(intent, templates["default"])

# ============ 主流程 ============

def process_email_cycle():
    """处理一轮邮件"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始邮件处理...")
    
    # 1. 连接 IMAP
    imap = connect_imap()
    if not imap:
        return
    
    # 2. 获取未读邮件
    emails = fetch_unread_emails(imap)
    print(f"获取到 {len(emails)} 封未读邮件")
    
    if not emails:
        imap.logout()
        return
    
    # 3. 连接 SMTP
    smtp = connect_smtp()
    if not smtp:
        imap.logout()
        return
    
    # 4. 处理每封邮件
    for email in emails:
        print(f"处理邮件: {email.subject[:50]}...")
        
        # AI 生成回复
        reply_body = generate_ai_reply(email)
        reply_subject = f"Re: {email.subject}"
        
        # 提取收件人邮箱
        import re
        match = re.search(r'[\w\.-]+@[\w\.-]+', email.from_email)
        to_email = match.group(0) if match else email.from_email
        
        # 发送回复
        if CONFIG["enable_review"]:
            print(f"  [审核模式] 待发送: {reply_subject}")
            # TODO: 写入审核队列
        else:
            if send_email(smtp, to_email, reply_subject, reply_body):
                print(f"  ✅ 已回复: {to_email}")
            else:
                print(f"  ❌ 发送失败: {to_email}")
    
    # 5. 清理连接
    smtp.quit()
    imap.logout()
    print("邮件处理完成")

def run_scheduler(interval_seconds=60):
    """定时运行"""
    print(f"🚀 邮件客服 MVP 启动 (间隔 {interval_seconds}s)")
    print("按 Ctrl+C 停止")
    
    try:
        while True:
            process_email_cycle()
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\n⏹️ 已停止")

# ============ 快速测试 ============

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 测试模式
        print("🧪 测试模式")
        
        test_email = Email(
            subject="Question about shipping",
            body="Hi, I want to know when my order will arrive? Order #12345",
            from_email="test@example.com",
            from_name="Test User",
            date="",
            message_id="test-001"
        )
        
        reply = generate_ai_reply(test_email)
        print("\n📧 测试邮件:")
        print(f"  Subject: {test_email.subject}")
        print(f"  Body: {test_email.body}")
        print(f"\n🤖 AI 回复:")
        print(reply)
    else:
        # 正常运行
        run_scheduler()