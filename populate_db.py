"""
Populate database with sample Categories, Industries, and Products.
Run with: python populate_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniworld.settings')
django.setup()

from product.models import Category, Industry, Product, Blog, Contact

# Clear existing data
Product.objects.all().delete()
Category.objects.all().delete()
Industry.objects.all().delete()
Blog.objects.all().delete()
Contact.objects.all().delete()

print("Creating Categories...")

# 2 Top-level Categories
cat_adhesives = Category.objects.create(name="Adhesives", slug="adhesives")
cat_chemicals = Category.objects.create(name="Chemicals", slug="chemicals")

# 2 Subcategories for Adhesives
cat_pu = Category.objects.create(name="PU Adhesives", slug="pu-adhesives", parent=cat_adhesives)
cat_rubber = Category.objects.create(name="Rubber Adhesives", slug="rubber-adhesives", parent=cat_adhesives)

# 2 Subcategories for Chemicals
cat_primers = Category.objects.create(name="Primers", slug="primers", parent=cat_chemicals)
cat_hardeners = Category.objects.create(name="Hardeners", slug="hardeners", parent=cat_chemicals)

print("Creating Industries...")

# 2 Top-level Industries
ind_footwear = Industry.objects.create(name="Footwear", slug="footwear")
ind_furniture = Industry.objects.create(name="Furniture", slug="furniture")

# 2 Sub-industries for Footwear
ind_sports = Industry.objects.create(name="Sports Shoes", slug="sports-shoes", parent=ind_footwear)
ind_leather = Industry.objects.create(name="Leather Shoes", slug="leather-shoes", parent=ind_footwear)

# 2 Sub-industries for Furniture
ind_wood = Industry.objects.create(name="Wood Furniture", slug="wood-furniture", parent=ind_furniture)
ind_upholstery = Industry.objects.create(name="Upholstery", slug="upholstery", parent=ind_furniture)

print("Creating Products...")

# Products in PU Adhesives subcategory
Product.objects.create(
    name="UniPU 500",
    slug="unipu-500",
    description="High-performance polyurethane adhesive for footwear applications.",
    applications="Shoe sole bonding, upper attachment",
    features="Heat resistant, flexible bond",
    category=cat_pu,
    industry=ind_sports,
    image="product/images/product/01.png",
    is_featured=True
)
Product.objects.create(
    name="UniPU 700",
    slug="unipu-700",
    description="Premium PU adhesive with enhanced durability.",
    applications="Heavy-duty footwear, industrial boots",
    features="Waterproof, extreme temperature resistance",
    category=cat_pu,
    industry=ind_leather,
    image="product/images/product/single01.png",
    is_featured=True
)

# Products in Rubber Adhesives subcategory
Product.objects.create(
    name="UniRubber Pro",
    slug="unirubber-pro",
    description="Professional grade rubber-based adhesive.",
    applications="Furniture assembly, foam bonding",
    features="Quick tack, strong initial bond",
    category=cat_rubber,
    industry=ind_wood,
    image="product/images/product/single02.png"
)
Product.objects.create(
    name="UniRubber Flex",
    slug="unirubber-flex",
    description="Flexible rubber adhesive for soft materials.",
    applications="Upholstery, fabric bonding",
    features="Remains flexible, no stiffening",
    category=cat_rubber,
    industry=ind_upholstery,
    image="product/images/product/single03.png"
)

# Products in Primers subcategory
Product.objects.create(
    name="UniPrime 100",
    slug="uniprime-100",
    description="Surface primer for enhanced adhesion.",
    applications="Wood surface preparation, laminate bonding",
    features="Fast drying, improves bond strength",
    category=cat_primers,
    industry=ind_wood,
    image="product/images/product/single04.png"
)

# Products in Hardeners subcategory
Product.objects.create(
    name="UniHard X",
    slug="unihard-x",
    description="Crosslinking hardener for two-component systems.",
    applications="Industrial adhesives, structural bonding",
    features="Controlled cure time, excellent flexibility",
    category=cat_hardeners,
    industry=ind_furniture,
    image="product/images/product/01.png"
)

print("Creating Blog Posts...")

from datetime import datetime, timedelta
from django.utils import timezone

# Create blog posts
Blog.objects.create(
    title="The Future of Industrial Adhesives: Trends and Innovations",
    slug="future-industrial-adhesives",
    content="The adhesive industry is evolving rapidly with new technologies and sustainable solutions. From bio-based adhesives to smart bonding systems, manufacturers are pushing the boundaries of what's possible. This article explores the latest trends shaping the future of industrial adhesives.",
    excerpt="Discover the latest trends and innovations transforming the industrial adhesive industry.",
    author="UniWorld Team",
    featured_image="product/images/blog-post/01.png",
    tags="adhesives, innovation, industry trends",
    published_date=timezone.now() - timedelta(days=5),
    is_published=True
)

Blog.objects.create(
    title="Sustainable Bonding Solutions for Modern Manufacturing",
    slug="sustainable-bonding-solutions",
    content="As environmental concerns grow, manufacturers are seeking eco-friendly adhesive solutions. Water-based adhesives, solvent-free formulations, and recyclable bonding systems are becoming the new standard. Learn how sustainable adhesives can reduce your carbon footprint without compromising performance.",
    excerpt="Explore eco-friendly adhesive solutions that deliver performance while protecting the environment.",
    author="UniWorld Team",
    featured_image="product/images/blog-post/02.png",
    tags="sustainability, eco-friendly, green manufacturing",
    published_date=timezone.now() - timedelta(days=12),
    is_published=True
)

Blog.objects.create(
    title="Choosing the Right Adhesive for Footwear Manufacturing",
    slug="adhesive-footwear-manufacturing",
    content="Footwear manufacturing requires specialized adhesives that can withstand flexing, temperature changes, and various materials. From PU adhesives for sole bonding to primers for leather preparation, selecting the right product is crucial for quality and durability.",
    excerpt="A comprehensive guide to selecting the perfect adhesive for footwear production.",
    author="UniWorld Team",
    featured_image="product/images/blog-post/03.png",
    tags="footwear, manufacturing, adhesives",
    published_date=timezone.now() - timedelta(days=20),
    is_published=True
)

Blog.objects.create(
    title="Quality Control in Adhesive Manufacturing: Best Practices",
    slug="quality-control-adhesive-manufacturing",
    content="Maintaining consistent quality in adhesive production requires rigorous testing and quality control protocols. From raw material inspection to final product testing, every step matters. This article outlines the best practices for ensuring adhesive quality and performance.",
    excerpt="Learn the essential quality control practices for adhesive manufacturing excellence.",
    author="UniWorld Team",
    featured_image="product/images/blog-post/01.png",
    tags="quality control, manufacturing, standards",
    published_date=timezone.now() - timedelta(days=28),
    is_published=True
)

Blog.objects.create(
    title="Understanding Polyurethane Adhesives: Properties and Applications",
    slug="understanding-polyurethane-adhesives",
    content="Polyurethane adhesives offer exceptional flexibility, strength, and resistance to environmental factors. They're widely used in automotive, construction, and footwear industries. This guide explains the chemistry, properties, and best applications for PU adhesives.",
    excerpt="A deep dive into polyurethane adhesives and their versatile applications.",
    author="UniWorld Team",
    featured_image="product/images/blog-post/02.png",
    tags="polyurethane, PU adhesives, technical guide",
    published_date=timezone.now() - timedelta(days=35),
    is_published=True
)

Blog.objects.create(
    title="Furniture Industry Adhesives: Trends and Solutions",
    slug="furniture-industry-adhesives",
    content="The furniture industry demands adhesives that provide strong bonds while meeting safety and environmental standards. From wood bonding to upholstery applications, modern adhesives offer solutions for every need. Explore the latest trends in furniture adhesives.",
    excerpt="Discover adhesive solutions tailored for the furniture manufacturing industry.",
    author="UniWorld Team",
    featured_image="product/images/blog-post/03.png",
    tags="furniture, wood adhesives, industry solutions",
    published_date=timezone.now() - timedelta(days=42),
    is_published=True
)

print("\n=== Summary ===")
print(f"Categories: {Category.objects.count()}")
print(f"  - Top-level: {Category.objects.filter(parent=None).count()}")
for cat in Category.objects.filter(parent=None):
    print(f"    - {cat.name}")
    for sub in cat.subcategories.all():
        print(f"      - {sub.name} ({sub.products.count()} products)")

print(f"\nIndustries: {Industry.objects.count()}")
print(f"  - Top-level: {Industry.objects.filter(parent=None).count()}")
for ind in Industry.objects.filter(parent=None):
    print(f"    - {ind.name}")
    for sub in ind.subindustries.all():
        print(f"      - {sub.name} ({sub.products.count()} products)")

print("Creating Contact Information...")

from product.models import Contact

Contact.objects.create(
    company_name="UniWorld Adhesives",
    factory_address="Dhaka-Sylhet Highway,\nMahona, Rupganj,\nNarayanganj",
    head_office_address="Family World Tower,\n2/6 Sir Syed Road,\nAsad Gate, Dhaka 1207",
    phone="+880 1234-567890",
    email="info@uniworldadhesives.com",
    working_hours="Sunday – Thursday, 9 AM – 6 PM",
    facebook_url="https://facebook.com/uniworld",
    instagram_url="https://instagram.com/uniworld",
    linkedin_url="https://linkedin.com/company/uniworld",
    twitter_url="https://twitter.com/uniworld",
    is_active=True
)

print(f"\nProducts: {Product.objects.count()}")
print(f"Blog Posts: {Blog.objects.count()}")
print(f"Contact Info: {Contact.objects.count()}")
print("\nDone!")
