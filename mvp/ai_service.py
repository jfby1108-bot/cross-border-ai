"""
AI 服务 - 支持多种 AI 提供商
"""
import requests
from config import config

class AIService:
    def __init__(self):
        self.provider = config.AI_PROVIDER
        
    def chat(self, message: str, system_prompt: str = "") -> str:
        """通用 AI 对话接口"""
        if self.provider == "openai":
            return self._openai_chat(message, system_prompt)
        elif self.provider == "minimax":
            return self._minimax_chat(message, system_prompt)
        elif self.provider == "ollama":
            return self._ollama_chat(message, system_prompt)
        else:
            return self._demo_response(message)
    
    def _openai_chat(self, message: str, system_prompt: str) -> str:
        """OpenAI GPT"""
        if not config.OPENAI_API_KEY:
            return self._demo_response(message)
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {config.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": config.OPENAI_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ]
                },
                timeout=30
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[OpenAI Error] {str(e)}"
    
    def _minimax_chat(self, message: str, system_prompt: str) -> str:
        """MiniMax AI"""
        if not config.MINIMAX_API_KEY:
            return self._demo_response(message)
        
        try:
            response = requests.post(
                "https://api.minimax.chat/v1/text/chatcompletion_pro",
                headers={
                    "Authorization": f"Bearer {config.MINIMAX_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": config.MINIMAX_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ]
                },
                timeout=30
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[MiniMax Error] {str(e)}"
    
    def _ollama_chat(self, message: str, system_prompt: str) -> str:
        """Ollama 本地 AI"""
        try:
            response = requests.post(
                f"{config.OLLAMA_URL}/api/chat",
                json={
                    "model": config.OLLAMA_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ]
                },
                timeout=60
            )
            return response.json()["message"]["content"]
        except Exception as e:
            return f"[Ollama Error] {str(e)}"
    
    def _demo_response(self, message: str) -> str:
        """Demo 模式回复"""
        return f"[Demo] AI 回复：{message}"
    
    def classify_intent(self, message: str) -> dict:
        """意图分类"""
        prompt = """你是一个客服意图分类器。根据用户消息判断意图。
        
可选意图：
- price_inquiry: 询问价格
- product_question: 产品问题
- purchase_intent: 购买意向
- complaint: 投诉
- general_inquiry: 一般咨询

只返回 JSON 格式：{"intent": "xxx", "confidence": 0.9}"""

        result = self.chat(message, prompt)
        
        # 简单解析
        try:
            import json
            return json.loads(result)
        except:
            return {"intent": "general_inquiry", "confidence": 0.5}

ai_service = AIService()
