# Listing 生成器 - MVP 版本

**功能**：根据产品信息，生成各平台 Listing  
**版本**：V1.0  
**日期**：2026-03-21

---

## 🎯 功能概述

用户输入产品基本信息 → 系统生成各平台 Listing

### 输入

```python
{
    "product_name": "Wireless Earbuds Pro",
    "brand": "Sony",
    "category": "Electronics",
    "features": [
        "Active Noise Cancellation",
        "30-hour battery",
        "Bluetooth 5.2",
        "Touch controls"
    ],
    "specifications": {
        "color": "Black",
        "model": "WH-1000XM5"
    },
    "target_markets": ["US", "UK", "DE", "JP"]
}
```

### 输出

```python
{
    "amazon": {
        "title": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones - 30 Hour Battery - Black",
        "bullet_points": [...],
        "description": "..."
    },
    "ebay": {
        "title": "Sony WH-1000XM5 Wireless Earbuds Pro - 30hr Battery - Black",
        "description": "..."
    },
    ...
}
```

---

## 📁 文件结构

```
product-description/
├── product_describer.py     # 原有的产品描述生成
├── listing_generator.py     # 新增：Listing 生成器
├── platform_templates.py    # 平台模板
├── requirements.txt         # 依赖更新
└── README.md               # 说明文档
```

---

## 🔧 代码实现

### 1. 平台模板 (platform_templates.py)

```python
AMAZON_TITLE_TEMPLATE = "{brand} {product_name} - {key_feature} - {color}"
AMAZON_BULLET_COUNT = 5

EBAY_TITLE_TEMPLATE = "{brand} {product_name} - {spec} - {color}"
EBAY_MAX_TITLE = 80
```

### 2. 生成器 (listing_generator.py)

```python
class ListingGenerator:
    def __init__(self):
        self.templates = PlatformTemplates()
    
    def generate(self, product_info):
        result = {}
        for market in product_info.get("target_markets", []):
            result[market] = self._generate_for_market(
                product_info, 
                market
            )
        return result
    
    def _generate_for_market(self, product_info, market):
        # 根据市场选择模板和语言
        ...
```

---

## 📊 支持的平台

| 平台 | 状态 | 语言 |
|------|------|------|
| Amazon US | ✅ | 英语 |
| Amazon UK | ✅ | 英语 |
| Amazon DE | ✅ | 德语 |
| Amazon JP | ✅ | 日语 |
| eBay | ✅ | 英语 |
| Walmart | 🔄 | 英语 |
| Rakuten | 🔄 | 日语 |

---

## 🚀 使用示例

```python
from listing_generator import ListingGenerator

generator = ListingGenerator()

product = {
    "product_name": "Wireless Earbuds Pro",
    "brand": "Sony",
    "features": ["ANC", "30h battery"],
    "target_markets": ["US", "DE", "JP"]
}

result = generator.generate(product)

print(result["amazon_us"]["title"])
# 输出：Sony Wireless Earbuds Pro - ANC - 30h Battery
```

---

## 📦 依赖

```bash
pip install qwen-client openai
```

---

## ⏳ 后续开发

- [ ] 图片处理（自动白底）
- [ ] CSV 批量导出
- [ ] Amazon SP API 上传
- [ ] 更多平台支持

---

*更新：2026-03-21*