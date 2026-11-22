from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category, Industry, Blog


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'index',
            'product',
            'technical_specs',
            'about',
            'rnd',
            'sustainability',
            'contact',
            'downloads',
            'industries_hub',
            'faq',
            'privacy_policy',
            'terms_of_use',
        ]

    def location(self, item):
        return reverse(item)


class ProductTypeSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.85

    def items(self):
        return ['adhesives', 'sealants', 'primers-cleaners', 'glues-diy']

    def location(self, item):
        return reverse('product_type_hub', args=[item])


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.85

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('category_products', args=[obj.slug.lower()])


class IndustrySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Industry.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('industry_products', args=[obj.slug.lower()])


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('single_product', args=[obj.slug])


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        posts = list(Blog.objects.filter(is_published=True))
        if len(posts) >= 3:
            return ['blog_index'] + posts
        return []

    def lastmod(self, obj):
        if obj == 'blog_index':
            return None
        return obj.updated_at

    def location(self, obj):
        if obj == 'blog_index':
            return reverse('blog')
        return reverse('blog_details', args=[obj.slug])