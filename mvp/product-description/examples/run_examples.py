"""
产品描述生成示例脚本
用于测试和演示 AI 产品描述功能
"""

import json
from product_describer import ProductDescriber


def load_examples():
    """加载示例数据"""
    with open("examples/products.json", "r", encoding="utf-8") as f:
        return json.load(f)


def run_example(describer: ProductDescriber, example: dict, example_name: str):
    """运行单个示例"""
    print(f"\n{'='*60}")
    print(f"📦 示例: {example_name}")
    print(f"{'='*60}")
    
    result = describer.describe(
        product_name=example["product"]["name"],
        category=example["product"]["category"],
        features=example["features"],
        target_market=example["target_market"],
        language=example["language"],
        tone=example["tone"]
    )
    
    print(f"\n🛍️ 产品: {result['product']['name']}")
    print(f"📂 类别: {result['product']['category']}")
    print(f"🎯 市场: {result['market']['target']}")
    print(f"🗣️ 语言: {result['output']['language']}")
    print(f"💼 语气: {result['output']['tone']}")
    
    print(f"\n📝 标题:")
    print(f"   {result['content']['title']}")
    
    print(f"\n📋 短描述:")
    print(f"   {result['content']['short_description']}")
    
    print(f"\n📖 长描述:")
    print(f"   {result['content']['long_description']}")
    
    print(f"\n🔍 SEO关键词:")
    print(f"   {result['content']['seo_keywords']}")
    
    return result


def demo_variants(describer: ProductDescriber):
    """演示多变体生成"""
    print(f"\n\n{'='*60}")
    print("🎨 变体描述示例")
    print(f"{'='*60}")
    
    variants = [
        {"color": "黑色", "size": "M"},
        {"color": "白色", "size": "M"},
        {"color": "黑色", "size": "L"},
    ]
    
    results = describer.describe_variants(
        product_name="Premium Cotton T-Shirt",
        category="Clothing > T-Shirts",
        base_features=[
            "100% organic cotton",
            "Soft and breathable",
            "Regular fit",
            "Machine washable"
        ],
        variants=variants,
        target_market="美国",
        language="en"
    )
    
    for i, result in enumerate(results):
        print(f"\n--- 变体 {i+1}: {result['variant']} ---")
        print(f"标题: {result['content']['title']}")
        print(f"描述: {result['content']['short_description']}")


def main():
    """主函数"""
    print("🚀 AI 产品描述生成器 - 示例演示")
    print("="*60)
    
    # 初始化（需要设置 QWEN_API_KEY 环境变量）
    try:
        describer = ProductDescriber()
    except ValueError as e:
        print(f"❌ 初始化失败: {e}")
        print("请设置 QWEN_API_KEY 环境变量")
        return
    
    # 加载示例
    examples = load_examples()
    
    # 运行示例
    for example_name, example in examples.items():
        try:
            run_example(describer, example, example_name)
        except Exception as e:
            print(f"❌ 示例 {example_name} 执行失败: {e}")
    
    # 变体演示
    demo_variants(describer)
    
    print(f"\n\n✅ 演示完成!")


if __name__ == "__main__":
    main()
