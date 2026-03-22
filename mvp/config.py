"""
SupportIQ 配置中心
所有 API Key 在这里配置
"""
import os
from typing import Optional

class Config:
    # ===== AI 配置 =====
    # 选择 AI 提供商: openai, minimax, ollama
    AI_PROVIDER = os.getenv("AI_PROVIDER", "demo")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # MiniMax
    MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
    MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "abab6.5s")
    
    # Ollama (本地免费)
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
    
    # ===== 邮件配置 =====
    # IMAP (收信)
    IMAP_HOST = os.getenv("IMAP_HOST", "")
    IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
    IMAP_USER = os.getenv("IMAP_USER", "")
    IMAP_PASSWORD = os.getenv("IMAP_PASSWORD", "")
    
    # SMTP (发信)
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    
    # ===== 微信配置 =====
    WECHAT_TOKEN = os.getenv("WECHAT_TOKEN", "")
    WECHAT_APPID = os.getenv("WECHAT_APPID", "")
    WECHAT_SECRET = os.getenv("WECHAT_SECRET", "")
    
    # ===== 数据库 (可选) =====
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    # ===== 应用配置 =====
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "supportiq-secret-key")

config = Config()
