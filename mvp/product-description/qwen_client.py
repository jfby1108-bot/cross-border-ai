"""
Qwen API 客户端
用于跨境电商产品描述生成
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List

import requests


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QwenAPIError(Exception):
    """Qwen API 错误"""
    pass


class QwenClient:
    """Qwen API 客户端封装"""
    
    # 支持的语言及对应模型
    LANGUAGE_MODELS = {
        "en": "qwen-turbo",
        "de": "qwen-turbo",
        "fr": "qwen-turbo",
        "es": "qwen-turbo",
        "it": "qwen-turbo",
        "ja": "qwen-turbo",
        "zh": "qwen-turbo",
        "pt": "qwen-turbo",
        "nl": "qwen-turbo",
        "ko": "qwen-turbo",
        "ar": "qwen-turbo",
        "ru": "qwen-turbo",
    }
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None,
        model: str = "qwen-turbo",
        timeout: int = 60
    ):
        """
        初始化 Qwen 客户端
        
        Args:
            api_key: API 密钥，默认从环境变量 QWEN_API_KEY 获取
            base_url: API 端点，默认从环境变量 QWEN_API_BASE 获取
            model: 使用的模型
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key or os.getenv("QWEN_API_KEY")
        self.base_url = base_url or os.getenv(
            "QWEN_API_BASE", 
            "https://dashscope.aliyuncs.com/api/v1"
        )
        self.model = model
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Set QWEN_API_KEY environment variable."
            )
        
        logger.info(f"QwenClient initialized with model: {self.model}")
    
    def _call_api(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        调用 Qwen API
        
        Args:
            prompt: 输入提示
            model: 模型名称（可选，默认使用实例的 model）
            temperature: 温度参数
            max_tokens: 最大 token 数
        
        Returns:
            API 响应文本
        
        Raises:
            QwenAPIError: API 调用失败时抛出
        """
        url = f"{self.base_url}/services/aigc/text-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model or self.model,
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "result_format": "message",
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        }
        
        try:
            logger.debug(f"Calling API with prompt length: {len(prompt)}")
            response = requests.post(
                url, 
                headers=headers, 
                json=payload, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "output" not in result or "choices" not in result["output"]:
                raise QwenAPIError(f"Invalid API response: {result}")
            
            return result["output"]["choices"][0]["message"]["content"]
            
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            raise QwenAPIError("API request timed out")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise QwenAPIError(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response: {e}")
            raise QwenAPIError(f"Failed to parse API response: {e}")
    
    def generate_product_description(
        self,
        product_name: str,
        product_features: List[str],
        target_market: str = "美国",
        language: str = "en",
        tone: str = "professional",
        include_seo: bool = True
    ) -> Dict[str, str]:
        """
        生成产品描述
        
        Args:
            product_name: 产品名称
            product_features: 产品特点列表
            target_market: 目标市场
            language: 输出语言 (en, de, fr, es, ja, pt, nl, ko, ar, ru等)
            tone: 语气 (professional, casual, luxury, persuasive)
            include_seo: 是否包含SEO优化
        
        Returns:
            包含 title, short_desc, long_desc, seo_keywords 的字典
        """
        logger.info(
            f"Generating description for: {product_name} "
            f"(market: {target_market}, lang: {language})"
        )
        
        # 构建 prompt
        prompt = self._build_prompt(
            product_name=product_name,
            product_features=product_features,
            target_market=target_market,
            language=language,
            tone=tone,
            include_seo=include_seo
        )
        
        # 调用 API
        try:
            result = self._call_api(
                prompt=prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            # 解析结果
            return self._parse_result(result)
        except QwenAPIError as e:
            logger.error(f"Failed to generate description: {e}")
            return {
                "title": "",
                "short_desc": "",
                "long_desc": "",
                "seo_keywords": "",
                "error": str(e)
            }
    
    def generate_bullet_points(
        self,
        product_name: str,
        product_features: List[str],
        language: str = "en",
        tone: str = "professional",
        num_points: int = 5
    ) -> List[str]:
        """
        生成产品要点（Bullet Points）
        
        Args:
            product_name: 产品名称
            product_features: 产品特点列表
            language: 输出语言
            tone: 语气风格
            num_points: 要点数量
        
        Returns:
            要点列表
        """
        logger.info(f"Generating bullet points for: {product_name}")
        
        features_text = "\n".join([f"- {f}" for f in product_features])
        
        prompt = f"""你是一个跨境电商产品描述专家。请为以下产品生成产品要点（Bullet Points）。

## 产品信息
- 产品名称: {product_name}
- 产品特点:
{features_text}
- 描述语言: {language}
- 语气风格: {tone}

请生成 {num_points} 个产品要点，每个要点应该：
- 简洁有力（20-50字）
- 突出产品卖点
- 适合电商平台展示
- 使用合适的语言风格

请直接输出JSON数组格式，例如：
["要点1", "要点2", "要点3"]

请直接输出JSON，不要其他内容。"""
        
        try:
            result = self._call_api(prompt=prompt, max_tokens=500)
            return self._parse_json_array(result)
        except QwenAPIError as e:
            logger.error(f"Failed to generate bullet points: {e}")
            return []
    
    def generate_marketing_copy(
        self,
        product_name: str,
        product_features: List[str],
        target_market: str = "美国",
        language: str = "en",
        copy_type: str = "social"  # social, email, ad
    ) -> Dict[str, str]:
        """
        生成营销文案
        
        Args:
            product_name: 产品名称
            product_features: 产品特点列表
            target_market: 目标市场
            language: 输出语言
            copy_type: 文案类型 (social: 社交媒体, email: 邮件, ad: 广告)
        
        Returns:
            包含不同长度文案的字典
        """
        logger.info(f"Generating marketing copy for: {product_name}")
        
        features_text = "\n".join([f"- {f}" for f in product_features])
        
        copy_type_desc = {
            "social": "社交媒体（Twitter/Facebook/Instagram）",
            "email": "营销邮件",
            "ad": "广告文案（Google/Facebook Ads）"
        }
        
        prompt = f"""你是一个跨境电商营销文案专家。请为以下产品生成营销文案。

## 产品信息
- 产品名称: {product_name}
- 产品特点:
{features_text}
- 目标市场: {target_market}
- 描述语言: {language}
- 文案类型: {copy_type_desc.get(copy_type, copy_type)}

请生成以下文案（JSON格式输出）：
{{
    "short": "短文案（20-50字，适合广告）",
    "medium": "中文文案（50-100字，适合社交媒体）",
    "long": "长文案（100-200字，适合邮件或落地页）"
}}

请直接输出JSON，不要其他内容。"""
        
        try:
            result = self._call_api(prompt=prompt, max_tokens=800)
            parsed = self._parse_json_dict(result)
            return parsed if parsed else {
                "short": "", "medium": "", "long": ""
            }
        except QwenAPIError as e:
            logger.error(f"Failed to generate marketing copy: {e}")
            return {"short": "", "medium": "", "long": "", "error": str(e)}
    
    def generate_social_media_post(
        self,
        product_name: str,
        product_features: List[str],
        platform: str = "instagram",
        language: str = "en",
        tone: str = "casual"
    ) -> Dict[str, str]:
        """
        生成社交媒体帖子
        
        Args:
            product_name: 产品名称
            product_features: 产品特点列表
            platform: 平台 (instagram, facebook, twitter, tiktok)
            language: 输出语言
            tone: 语气风格
        
        Returns:
            包含标题、正文、标签的字典
        """
        logger.info(f"Generating social media post for: {product_name}")
        
        features_text = "\n".join([f"- {f}" for f in product_features])
        
        platform_desc = {
            "instagram": "Instagram（图片为主，可带多标签）",
            "facebook": "Facebook（可较长，鼓励互动）",
            "twitter": "Twitter/X（简洁，280字内）",
            "tiktok": "TikTok（短视频配文）"
        }
        
        prompt = f"""你是一个社交媒体营销专家。请为以下产品生成社交媒体帖子。

## 产品信息
- 产品名称: {product_name}
- 产品特点:
{features_text}
- 平台: {platform_desc.get(platform, platform)}
- 语言: {language}
- 风格: {tone}

请生成以下内容（JSON格式输出）：
{{
    "title": "吸引眼球的标题（可选）",
    "body": "正文内容",
    "hashtags": "标签（用空格分隔）",
    "cta": "行动号召（可选）"
}}

请直接输出JSON，不要其他内容。"""
        
        try:
            result = self._call_api(prompt=prompt, max_tokens=600)
            parsed = self._parse_json_dict(result)
            return parsed if parsed else {
                "title": "", "body": "", "hashtags": "", "cta": ""
            }
        except QwenAPIError as e:
            logger.error(f"Failed to generate social post: {e}")
            return {
                "title": "", "body": "", "hashtags": "", "cta": "",
                "error": str(e)
            }
    
    def _build_prompt(
        self,
        product_name: str,
        product_features: List[str],
        target_market: str,
        language: str,
        tone: str,
        include_seo: bool
    ) -> str:
        """构建产品描述的提示词"""
        
        features_text = "\n".join([f"- {f}" for f in product_features])
        
        seo_instruction = ""
        if include_seo:
            seo_instruction = """
重要：需要包含 SEO 优化关键词，适合电商平台搜索排名。
"""
        
        prompt = f"""你是一个跨境电商产品描述专家。请为以下产品生成专业的产品描述。

## 产品信息
- 产品名称: {product_name}
- 产品特点:
{features_text}
- 目标市场: {target_market}
- 描述语言: {language}
- 语气风格: {tone}
{seo_instruction}

请生成以下内容（JSON格式输出）：
{{
    "title": "产品标题（简洁有力，包含关键词，50-80字符）",
    "short_desc": "短描述（50-100字，适合列表页）",
    "long_desc": "长描述（150-300字，适合详情页，包含卖点和使用场景）",
    "seo_keywords": "SEO关键词（用逗号分隔，5-10个关键词）"
}}

请直接输出JSON，不要其他内容。"""
        
        return prompt
    
    def _parse_result(self, result: str) -> Dict[str, str]:
        """解析 API 返回的 JSON 结果"""
        try:
            result = result.strip()
            
            # 移除 markdown 代码块标记
            if result.startswith("```json"):
                result = result[7:]
            elif result.startswith("```"):
                result = result[3:]
            
            if result.endswith("```"):
                result = result[:-3]
            
            return json.loads(result.strip())
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON, attempting fallback: {e}")
            return {
                "title": "",
                "short_desc": result,
                "long_desc": result,
                "seo_keywords": ""
            }
    
    def _parse_json_array(self, result: str) -> List[str]:
        """解析 JSON 数组结果"""
        try:
            result = result.strip()
            
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            
            if result.endswith("```"):
                result = result[:-3]
            
            parsed = json.loads(result.strip())
            
            if isinstance(parsed, list):
                return parsed
            elif isinstance(parsed, dict) and "items" in parsed:
                return parsed["items"]
            else:
                return []
                
        except (json.JSONDecodeError, IndexError) as e:
            logger.warning(f"Failed to parse JSON array: {e}")
            return []
    
    def _parse_json_dict(self, result: str) -> Dict[str, str]:
        """解析 JSON 对象结果"""
        try:
            result = result.strip()
            
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            
            if result.endswith("```"):
                result = result[:-3]
            
            parsed = json.loads(result.strip())
            
            if isinstance(parsed, dict):
                return parsed
            else:
                return {}
                
        except (json.JSONDecodeError, IndexError) as e:
            logger.warning(f"Failed to parse JSON dict: {e}")
            return {}


# ==================== 便捷函数 ====================

def generate_description(
    product_name: str,
    product_features: List[str],
    target_market: str = "美国",
    language: str = "en",
    **kwargs
) -> Dict[str, str]:
    """快速生成产品描述的便捷函数"""
    client = QwenClient()
    return client.generate_product_description(
        product_name=product_name,
        product_features=product_features,
        target_market=target_market,
        language=language,
        **kwargs
    )


def generate_bullet_points(
    product_name: str,
    product_features: List[str],
    language: str = "en",
    **kwargs
) -> List[str]:
    """快速生成产品要点的便捷函数"""
    client = QwenClient()
    return client.generate_bullet_points(
        product_name=product_name,
        product_features=product_features,
        language=language,
        **kwargs
    )
