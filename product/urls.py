from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from . import views
from .inquiry_views import submit_inquiry
from .sitemaps import (
    StaticViewSitemap,
    CategorySitemap,
    IndustrySitemap,
    ProductTypeSitemap,
    ProductSitemap,
    BlogSitemap,
)

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'industries': IndustrySitemap,
    'product_types': ProductTypeSitemap,
    'products': ProductSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    # Core Pages
    path('', views.index, name='index'),
    path('product/', views.product_list, name='product'),
    path('technical-specs/', views.technical_specs, name='technical_specs'),
    
    # 301 Redirects for Misleading & Case-Sensitive URLs
    path(
        'product/primer-pupvc/',
        RedirectView.as_view(url='/product/polyurethane-adhesive/', permanent=True),
    ),
    re_path(
        r'^product/category/(?P<slug>.*[A-Z].*)/$',
        views.category_case_redirect,
        name='category_case_redirect',
    ),
    
    # Product-Type Hubs, Category, Industry & Product Detail
    path('product/type/<slug:type_slug>/', views.product_type_hub, name='product_type_hub'),
    path('product/category/<slug:slug>/', views.category_products, name='category_products'),
    path('product/<slug:slug>/', views.product_detail, name='single_product'),
    path('industries/', views.industries_hub, name='industries_hub'),
    path('industry/<slug:slug>/', views.industry_products, name='industry_products'),
    
    # Content & Trust Pages
    path('about/', views.about, name='about'),
    path('rnd/', views.rnd, name='rnd'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq_page, name='faq'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    
    # Blog
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_details'),
    
    # Downloads (SEO-friendly PDF slug + Legacy UUID support)
    path('downloads/', views.downloads, name='downloads'),
    path('downloads/<slug:slug>.pdf', views.download_file_by_slug, name='download_file_slug'),
    path('download/<uuid:uuid>/', views.download_file, name='download_file'),
    
    # Inquiry API
    path('inquiry/submit/', submit_inquiry, name='submit_inquiry'),
    
    # Technical SEO: XML Sitemap & robots.txt
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]