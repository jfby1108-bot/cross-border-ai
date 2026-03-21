# AI 产品描述生成器

跨境电商 MVP - 基于 Qwen API 的产品描述自动生成

## 功能特性

- ✨ 自动生成多语言产品描述
- 🎯 支持多个目标市场（美国、欧洲、日本等）
- 📝 支持多种语气风格（专业、休闲、奢华）
- 🔍 内置 SEO 关键词优化
- 📦 支持产品变体描述生成
- 🔌 易于集成的 Python API

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置 API Key

```bash
export QWEN_API_KEY="your-api-key-here"
```

### 3. 使用示例

```python
from product_describer import ProductDescriber

# 初始化
describer = ProductDescriber()

# 生成产品描述
result = describer.describe(
    product_name="Wireless Earbuds Pro",
    category="Electronics > Audio",
    features=[
        "Active Noise Cancellation",
        "30-hour battery life",
        "Premium sound quality"
    ],
    target_market="美国",
    language="en",
    tone="professional"
)

print(result["content"]["title"])
print(result["content"]["long_description"])
```

## 项目结构

```
product-description/
├── ARCHITECTURE.md      # 技术架构文档
├── config.yaml          # 配置文件
├── qwen_client.py       # Qwen API 客户端
├── product_describer.py # 产品描述生成器
├── requirements.txt     # Python 依赖
├── README.md            # 说明文档
└── examples/
    ├── products.json    # 示例数据
    └── run_examples.py  # 示例脚本
```

## API 参考

### ProductDescriber

主类，用于生成产品描述

#### 方法

##### `describe(product_name, category, features, target_market, language, tone)`

生成单个产品描述

**参数:**
- `product_name` (str): 产品名称
- `category` (str): 产品类别
- `features` (List[str]): 产品特点列表
- `target_market` (str): 目标市场，默认 "美国"
- `language` (str): 输出语言，默认 "en"
- `tone` (str): 语气风格，默认 "professional"

**返回:**
- Dict 包含 title, short_description, long_description, seo_keywords

##### `describe_variants(product_name, category, base_features, variants, target_market, language)`

生成多变体产品描述

## 支持的市场

| 市场 | 平台 | 语言 |
|------|------|------|
| 美国 | Amazon, eBay, Walmart | en |
| 欧洲 | Amazon EU, Allegro | de/fr/es |
| 英国 | Amazon UK, eBay UK | en |
| 日本 | Amazon JP, Rakuten | ja |

## 支持的语言

- `en` - English
- `de` - German
- `fr` - French  
- `es` - Spanish
- `it` - Italian
- `ja` - Japanese
- `zh` - Chinese

## 语气风格

- `professional` - 专业、正式
- `casual` - 轻松、友好
- `luxury` - 高端、奢华
- `persuasive` - 有说服力

## License

MIT
