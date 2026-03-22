"""
邮件服务 - 支持 SMTP 发送
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config

class EmailService:
    def __init__(self):
        self.smtp_host = config.SMTP_HOST
        self.smtp_port = config.SMTP_PORT
        self.smtp_user = config.SMTP_USER
        self.smtp_password = config.SMTP_PASSWORD
    
    def send_reply(self, to_email: str, subject: str, body: str, html: str = None) -> dict:
        """发送回复邮件"""
        if not self.smtp_host or not self.smtp_user:
            return self._demo_send(to_email, subject, body)
        
        try:
            # 创建邮件
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.smtp_user
            msg["To"] = to_email
            
            # 添加纯文本和 HTML 版本
            if body:
                msg.attach(MIMEText(body, "plain", "utf-8"))
            if html:
                msg.attach(MIMEText(html, "html", "utf-8"))
            
            # 发送邮件
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return {"success": True, "message": "邮件发送成功"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _demo_send(self, to_email: str, subject: str, body: str) -> dict:
        """Demo 模式"""
        return {
            "success": True, 
            "mode": "demo",
            "message": f"[Demo] 邮件已发送 (未配置 SMTP)",
            "to": to_email,
            "subject": subject
        }
    
    def check_new_emails(self) -> list:
        """检查新邮件 (需要 IMAP 配置)"""
        if not config.IMAP_HOST or not config.IMAP_USER:
            return []
        
        # TODO: 实现 IMAP 收信
        return []

email_service = EmailService()
