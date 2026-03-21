"""
AI 产品描述生成器
跨境电商 MVP - 基于 Qwen API 的产品描述自动生成
"""

import logging
from typing import List, Dict, Optional, Any

from qwen_client import QwenClient, QwenAPIError


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProductDescriber:
    """产品描述生成器"""
    
    # 支持的市场
    MARKETS: Dict[str, str] = {
        "美国": "Amazon, eBay, Walmart, Target",
        "欧洲": "Amazon EU, eBay, Allegro",
        "英国": "Amazon UK, eBay UK, ASDA",
        "德国": "Amazon DE, eBay DE, Otto",
        "法国": "Amazon FR, Cdiscount",
        "西班牙": "Amazon ES, Miravia",
        "意大利": "Amazon IT, eBay IT",
        "日本": "Amazon JP, Rakuten, Yahoo! Japan",
        "澳大利亚": "Amazon AU, eBay AU",
        "加拿大": "Amazon CA, eBay CA",
        "巴西": "Amazon BR, Mercado Livre",
        "印度": "Amazon IN, Flipkart"
    }
    
    # 支持的语言 (ISO 639-1 代码)
    LANGUAGES: Dict[str, Dict[str, str]] = {
        "en": {"name": "English", "native": "English", "region": "US/UK"},
        "de": {"name": "German", "native": "Deutsch", "region": "DE"},
        "fr": {"name": "French", "native": "Français", "region": "FR"},
        "es": {"name": "Spanish", "native": "Español", "region": "ES"},
        "it": {"name": "Italian", "native": "Italiano", "region": "IT"},
        "ja": {"name": "Japanese", "native": "日本語", "region": "JP"},
        "zh": {"name": "Chinese", "native": "中文", "region": "CN"},
        "pt": {"name": "Portuguese", "native": "Português", "region": "BR/PT"},
        "nl": {"name": "Dutch", "native": "Nederlands", "region": "NL"},
        "ko": {"name": "Korean", "native": "한국어", "region": "KR"},
        "ar": {"name": "Arabic", "native": "العربية", "region": "Middle East"},
        "ru": {"name": "Russian", "native": "Русский", "region": "RU"},
    }
    
    # 语气风格
    TONES: Dict[str, str] = {
        "professional": "专业、正式、权威",
        "casual": "轻松、友好、亲切",
        "luxury": "高端、奢华、精致",
        "persuasive": "有说服力、激励行动"
    }
    
    # 社交媒体平台
    SOCIAL_PLATFORMS: List[str] = [
        "instagram", "facebook", "twitter", "tiktok", "pinterest"
    ]
    
    # 文案类型
    COPY_TYPES: List[str] = ["social", "email", "ad"]
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model: str = "qwen-turbo",
        timeout: int = 60
    ):
        """
        初始化
        
        Args:
            api_key: Qwen API 密钥
            model: 使用的模型
            timeout: 请求超时时间
        """
        self.client = QwenClient(
            api_key=api_key,
            model=model,
            timeout=timeout
        )
        logger.info("ProductDescriber initialized")
    
    def describe(
        self,
        product_name: str,
        category: str,
        features: List[str],
        target_market: str = "美国",
        language: str = "en",
        tone: str = "professional",
        platform: Optional[str] = None,
        include_seo: bool = True
    ) -> Dict[str, Any]:
        """
        生成完整的产品描述套件
        
        Args:
            product_name: 产品名称
            category: 产品类别
            features: 产品特点列表
            target_market: 目标市场
            language: 输出语言代码 (en, de, fr, es, it, ja, zh, pt, nl, ko, ar, ru)
            tone: 语气风格 (professional, casual, luxury, persuasive)
            platform: 电商平台（可选）
            include_seo: 是否包含SEO优化
        
        Returns:
            完整的描述套件
        
        Raises:
            ValueError: 参数无效时抛出
        """
        # 验证语言
        if language not in self.LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Supported: {list(self.LANGUAGES.keys())}"
            )
        
        # 验证语气
        if tone not in self.TONES:
            raise ValueError(
                f"Unsupported tone: {tone}. "
                f"Supported: {list(self.TONES.keys())}"
            )
        
        # 确定平台
        if not platform:
            platform = self.MARKETS.get(target_market, "Amazon, eBay")
        
        logger.info(
            f"Generating description for '{product_name}' "
            f"(market: {target_market}, lang: {language})"
        )
        
        # 调用 Qwen API
        try:
            result = self.client.generate_product_description(
                product_name=product_name,
                product_features=features,
                target_market=target_market,
                language=language,
                tone=tone,
                include_seo=include_seo
            )
        except QwenAPIError as e:
            logger.error(f"Failed to generate description: {e}")
            return {
                "success": False,
                "error": str(e),
                "product": {
                    "name": product_name,
                    "category": category,
                    "features": features
                }
            }
        
        # 组装完整结果
        return {
            "success": True,
            "product": {
                "name": product_name,
                "category": category,
                "features": features
            },
            "market": {
                "target": target_market,
                "platform": platform
            },
            "output": {
                "language": self.LANGUAGES[language]["name"],
                "language_native": self.LANGUAGES[language]["native"],
                "tone": self.TONES[tone]
            },
            "content": {
                "title": result.get("title", ""),
                "short_description": result.get("short_desc", ""),
                "long_description": result.get("long_desc", ""),
                "seo_keywords": result.get("seo_keywords", "")
            }
        }
    
    def describe_bullet_points(
        self,
        product_name: str,
        features: List[str],
        language: str = "en",
        tone: str = "professional",
        num_points: int = 5
    ) -> Dict[str, Any]:
        """
        生成产品要点（Bullet Points）
        
        Args:
            product_name: 产品名称
            features: 产品特点列表
            language: 输出语言
            tone: 语气风格
            num_points: 要点数量
        
        Returns:
            要点结果
        """
        logger.info(f"Generating bullet points for '{product_name}'")
        
        try:
            bullet_points = self.client.generate_bullet_points(
                product_name=product_name,
                product_features=features,
                language=language,
                tone=tone,
                num_points=num_points
            )
            
            return {
                "success": True,
                "product": {"name": product_name},
                "language": self.LANGUAGES.get(language, {}).get("name", language),
                "bullet_points": bullet_points,
                "count": len(bullet_points)
            }
        except QwenAPIError as e:
            logger.error(f"Failed to generate bullet points: {e}")
            return {
                "success": False,
                "error": str(e),
                "bullet_points": []
            }
    
    def describe_marketing_copy(
        self,
        product_name: str,
        features: List[str],
        target_market: str = "美国",
        language: str = "en",
        copy_type: str = "social"
    ) -> Dict[str, Any]:
        """
        生成营销文案
        
        Args:
            product_name: 产品名称
            features: 产品特点列表
            target_market: 目标市场
            language: 输出语言
            copy_type: 文案类型 (social, email, ad)
        
        Returns:
            营销文案结果
        """
        logger.info(f"Generating marketing copy for '{product_name}'")
        
        if copy_type not in self.COPY_TYPES:
            raise ValueError(
                f"Unsupported copy type: {copy_type}. "
                f"Supported: {self.COPY_TYPES}"
            )
        
        try:
            result = self.client.generate_marketing_copy(
                product_name=product_name,
                product_features=features,
                target_market=target_market,
                language=language,
                copy_type=copy_type
            )
            
            return {
                "success": True,
                "product": {"name": product_name},
                "market": target_market,
                "copy_type": copy_type,
                "content": result
            }
        except QwenAPIError as e:
            logger.error(f"Failed to generate marketing copy: {e}")
            return {
                "success": False,
                "error": str(e),
                "content": {}
            }
    
    def describe_social_media(
        self,
        product_name: str,
        features: List[str],
        platform: str = "instagram",
        language: str = "en",
        tone: str = "casual"
    ) -> Dict[str, Any]:
        """
        生成社交媒体帖子
        
        Args:
            product_name: 产品名称
            features: 产品特点列表
            platform: 社交平台 (instagram, facebook, twitter, tiktok)
            language: 输出语言
            tone: 语气风格
        
        Returns:
            社交媒体帖子结果
        """
        logger.info(f"Generating social media post for '{product_name}'")
        
        if platform not in self.SOCIAL_PLATFORMS:
            raise ValueError(
                f"Unsupported platform: {platform}. "
                f"Supported: {self.SOCIAL_PLATFORMS}"
            )
        
        try:
            result = self.client.generate_social_media_post(
                product_name=product_name,
                product_features=features,
                platform=platform,
                language=language,
                tone=tone
            )
            
            return {
                "success": True,
                "product": {"name": product_name},
                "platform": platform,
                "content": result
            }
        except QwenAPIError as e:
            logger.error(f"Failed to generate social post: {e}")
            return {
                "success": False,
                "error": str(e),
                "content": {}
            }
    
    def describe_variants(
        self,
        product_name: str,
        category: str,
        base_features: List[str],
        variants: List[Dict[str, str]],
        target_market: str = "美国",
        language: str = "en",
        tone: str = "professional"
    ) -> List[Dict[str, Any]]:
        """
        生成多变体产品描述
        
        Args:
            product_name: 产品名称
            category: 产品类别
            base_features: 基础特点
            variants: 变体列表 [{"color": "红色", "size": "M"}, ...]
            target_market: 目标市场
            language: 输出语言
            tone: 语气风格
        
        Returns:
            变体描述列表
        """
        logger.info(f"Generating variant descriptions for '{product_name}'")
        
        results = []
        
        for i, variant in enumerate(variants):
            logger.info(f"Processing variant {i+1}/{len(variants)}: {variant}")
            
            # 合并基础特点和变体特点
            variant_features = base_features.copy()
            for key, value in variant.items():
                variant_features.append(f"{key}: {value}")
            
            # 生成描述
            result = self.describe(
                product_name=product_name,
                category=category,
                features=variant_features,
                target_market=target_market,
                language=language,
                tone=tone
            )
            
            result["variant"] = variant
            results.append(result)
        
        return results
    
    def describe_all_formats(
        self,
        product_name: str,
        category: str,
        features: List[str],
        target_market: str = "美国",
        language: str = "en",
        tone: str = "professional"
    ) -> Dict[str, Any]:
        """
        生成所有格式的产品描述
        
        一次性生成：标准描述、要点、营销文案、社交媒体
        
        Args:
            product_name: 产品名称
            category: 产品类别
            features: 产品特点列表
            target_market: 目标市场
            language: 输出语言
            tone: 语气风格
        
        Returns:
            包含所有格式的完整结果
        """
        logger.info(f"Generating all formats for '{product_name}'")
        
        # 标准产品描述
        main_desc = self.describe(
            product_name=product_name,
            category=category,
            features=features,
            target_market=target_market,
            language=language,
            tone=tone
        )
        
        # 产品要点
        bullet_points = self.describe_bullet_points(
            product_name=product_name,
            features=features,
            language=language,
            tone=tone
        )
        
        # 营销文案
        marketing_copy = self.describe_marketing_copy(
            product_name=product_name,
            features=features,
            target_market=target_market,
            language=language,
            copy_type="social"
        )
        
        # 社交媒体
        social = self.describe_social_media(
            product_name=product_name,
            features=features,
            platform="instagram",
            language=language,
            tone=tone
        )
        
        return {
            "product": {
                "name": product_name,
                "category": category,
                "features": features
            },
            "market": target_market,
            "language": language,
            "tone": tone,
            "formats": {
                "main_description": main_desc,
                "bullet_points": bullet_points,
                "marketing_copy": marketing_copy,
                "social_media": social
            }
        }
    
    @classmethod
    def get_supported_languages(cls) -> Dict[str, Dict[str, str]]:
        """获取支持的语言列表"""
        return cls.LANGUAGES
    
    @classmethod
    def get_supported_markets(cls) -> Dict[str, str]:
        """获取支持的市场列表"""
        return cls.MARKETS
    
    @classmethod
    def get_supported_tones(cls) -> Dict[str, str]:
        """获取支持的语气风格列表"""
        return cls.TONES


# ==================== 示例用法 ====================

if __name__ == "__main__":
    # 初始化
    describer = ProductDescriber()
    
    # 示例产品
    product = {
        "name": "Wireless Bluetooth Earbuds Pro",
        "category": "Electronics > Audio > Headphones",
        "features": [
            "Active Noise Cancellation (ANC)",
            "30-hour total battery life with charging case",
            "Premium 13mm drivers for high-quality sound",
            "Ergonomic in-ear design for comfortable fit",
            "Intuitive touch controls",
            "IPX5 water resistance",
            "Fast charging support"
        ]
    }
    
    # 测试不同语言
    languages = ["en", "de", "ja"]
    
    for lang in languages:
        print(f"\n{'='*50}")
        print(f"Language: {lang}")
        print('='*50)
        
        result = describer.describe(
            product_name=product["name"],
            category=product["category"],
            features=product["features"],
            target_market="美国",
            language=lang,
            tone="professional"
        )
        
        if result.get("success"):
            print(f"标题: {result['content']['title']}")
            print(f"\n短描述: {result['content']['short_description']}")
            print(f"\n长描述: {result['content']['long_description']}")
            print(f"\nSEO关键词: {result['content']['seo_keywords']}")
        else:
            print(f"Error: {result.get('error')}")
