from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, HttpResponse
from django.urls import reverse
from .models import Product, Blog, Category, Industry, DownloadCategory, DownloadFile


PRODUCT_TYPE_CONFIG = {
    'adhesives': {
        'name': 'Industrial Adhesives',
        'h1': 'Industrial Adhesives (PU, SBS Spray, Graft CR & Synthetic Rubber)',
        'meta_title': 'Industrial Adhesives: PU, SBS Spray & Graft CR | Uniworld',
        'meta_description': 'Explore Uniworld industrial adhesives: Polyurethane (PU), Graft CR chloroprene, SBS sprayable, and synthetic rubber contact adhesives made in Bangladesh.',
        'intro': 'High-strength solvent-based adhesives engineered for footwear sole bonding, foam and mattress lamination, woodworking, and automotive trim across Bangladesh.',
        'slugs': [
            'sbs-sprayable-adhesive',
            'sbs-sprayable-adhesive-white-sb602',
            'synthetic-rubber-adhesive',
            'graft-adhesive',
            'polyurethane-adhesive',
            'polyurethane-adhesive-premium',
        ],
    },
    'sealants': {
        'name': 'Silicone & Construction Sealants',
        'h1': 'Silicone & Construction Sealants (Acetic, Neutral & Nail Free)',
        'meta_title': 'Silicone & Construction Sealants in Bangladesh | Uniworld',
        'meta_description': 'Weatherproof acetic and neutral cure silicone sealants plus heavy-duty Nail Free construction adhesive in 300 ml cartridges for glazing, mirrors, and trade.',
        'intro': 'One-component RTV silicone sealants and high-grab Nail Free construction adhesives formulated for glass facades, sanitary ware, mirrors, aluminum, and masonry.',
        'slugs': [
            'silicone-sealant',
            'silicone-sealant-neutral',
            'nail-free-sealant',
        ],
    },
    'primers-cleaners': {
        'name': 'Surface Primers & Cleaners',
        'h1': 'Surface Primers & Sole Cleaners (EVA, PU/PVC & Synthetic Cleaner)',
        'meta_title': 'EVA & PU/PVC Primers and Synthetic Sole Cleaner | Uniworld',
        'meta_description': 'Boost sole-to-upper bond strength with Uniworld EVA Primer, PU/PVC Primer, and fast-evaporating Synthetic Cleaner for footwear and synthetic leather.',
        'intro': 'Essential surface preparation chemistry that removes mold-release oils and activates low-surface-energy EVA, Phylon, PU, PVC, and TPR substrates prior to bonding.',
        'slugs': [
            'pupvc-primer',
            'eva-primer',
            'synthetic-cleaner',
        ],
    },
    'glues-diy': {
        'name': 'Instant Glues, Spray Paint & DIY',
        'h1': 'Instant Super Glue, Aerosol Spray Paint & Hardware Specialties',
        'meta_title': 'Super Glue, Aerosol Spray Paint & Hardware Glues | Uniworld',
        'meta_description': 'Fast-curing cyanoacrylate super glue, 400 ml aerosol spray paint, and high-tack rat glue for hardware retail, trade repairs, and DIY use across Bangladesh.',
        'intro': 'Retail-ready instant bonding adhesives, fast-drying acrylic spray coatings, and high-tack pest-control adhesives built for hardware stores and daily maintenance.',
        'slugs': [
            'cyanoacrylate-super-glue',
            'aerosol-spray-paint',
            'rat-glue',
        ],
    },
}


def robots_txt(request):
    """Serve SEO-friendly robots.txt with Sitemap reference."""
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /ckeditor/",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def category_case_redirect(request, slug):
    """301 Permanent Redirect from capitalized category URLs to lowercase."""
    return redirect('category_products', slug=slug.lower(), permanent=True)


def index(request):
    """Home page with featured products, categories, industries and recent blog posts."""
    featured_products = Product.objects.filter(is_featured=True).prefetch_related('images')[:8]
    all_products = Product.objects.all().prefetch_related('images')
    categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('subcategories')
    industries = Industry.objects.filter(parent=None, is_active=True)
    recent_posts = Blog.objects.filter(is_published=True).order_by('-published_date')[:3]

    context = {
        'featured_products': featured_products,
        'all_products': all_products,
        'categories': categories,
        'industries': industries,
        'recent_posts': recent_posts,
        'show_blog_section': recent_posts.count() >= 3,
        'meta_title': 'Adhesive & Sealant Manufacturer in Bangladesh | Uniworld',
        'meta_description': 'ISO 9001:2015 certified maker of industrial adhesives, sealants, primers and cleaners for footwear, furniture and hardware. Made in Bangladesh. Get a quote.',
    }
    return render(request, 'index.html', context)


def product_list(request):
    """Product listing page - show all products without ?from= duplicate params."""
    products = Product.objects.all().select_related('category', 'industry').prefetch_related('images')
    all_categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('subcategories')
    all_industries = Industry.objects.filter(parent=None, is_active=True).prefetch_related('subindustries')

    context = {
        'products': products,
        'filter_type': 'all',
        'all_categories': all_categories,
        'all_industries': all_industries,
        'meta_title': 'Industrial Adhesives, Sealants & Primers | Uniworld',
        'meta_description': 'Browse 15 Uniworld products: SBS, PU, synthetic rubber and graft adhesives, silicone sealants, primers, super glue and cleaners. Bulk supply across Bangladesh.',
    }
    return render(request, 'product.html', context)


def product_type_hub(request, type_slug):
    """Product-Type Hub pages: Adhesives, Sealants, Primers & Cleaners, Glues & DIY."""
    if any(c.isupper() for c in type_slug):
        return redirect('product_type_hub', type_slug=type_slug.lower(), permanent=True)

    config = PRODUCT_TYPE_CONFIG.get(type_slug.lower())
    if not config:
        raise Http404("Product type not found")

    products = Product.objects.filter(slug__in=config['slugs']).select_related('category', 'industry').prefetch_related('images')
    all_categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('subcategories')
    all_industries = Industry.objects.filter(parent=None, is_active=True).prefetch_related('subindustries')

    context = {
        'products': products,
        'filter_type': 'product_type',
        'active_type': type_slug.lower(),
        'type_hub': config,
        'all_categories': all_categories,
        'all_industries': all_industries,
        'meta_title': config['meta_title'],
        'meta_description': config['meta_description'],
    }
    return render(request, 'product.html', context)


def technical_specs(request):
    """Dedicated Engineering & Technical Specifications Comparison Page (Reference Design)."""
    products = Product.objects.all().select_related('category', 'industry').prefetch_related('images')
    context = {
        'products': products,
        'meta_title': 'Adhesive Technical Specifications & Grade Chart | Uniworld',
        'meta_description': 'Compare viscosity, open time, cure time, peel strength and substrates across Uniworld SBS, Polyurethane (PU), Graft CR and Synthetic Rubber adhesives.',
    }
    return render(request, 'technical_specs.html', context)


def product_detail(request, slug):
    """Product detail page - clean canonical URL, breadcrumb handled via sessionStorage."""
    if 'from' in request.GET:
        return redirect('single_product', slug=slug, permanent=True)

    product = get_object_or_404(Product.objects.select_related('category', 'industry').prefetch_related('images'), slug=slug)

    manual_related = list(product.related_products_manual.all().prefetch_related('images'))
    if manual_related:
        related_products = manual_related[:4]
    elif product.category:
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(uuid=product.uuid).prefetch_related('images')[:4]
    else:
        related_products = Product.objects.exclude(uuid=product.uuid).prefetch_related('images')[:4]

    context = {
        'product': product,
        'related_products': related_products,
        'meta_title': product.display_meta_title,
        'meta_description': product.meta_description or product.description[:158],
    }
    return render(request, 'single_product.html', context)


def category_products(request, slug):
    """Category products page with unique buying guide and FAQs."""
    if any(c.isupper() for c in slug):
        return redirect('category_products', slug=slug.lower(), permanent=True)

    category = get_object_or_404(Category, slug__iexact=slug, is_active=True)

    category_ids = [category.pk]
    for subcategory in category.subcategories.filter(is_active=True):
        category_ids.append(subcategory.pk)

    products = Product.objects.filter(category__pk__in=category_ids).select_related('category', 'industry').prefetch_related('images')
    all_categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('subcategories')
    all_industries = Industry.objects.filter(parent=None, is_active=True).prefetch_related('subindustries')

    context = {
        'products': products,
        'category': category,
        'filter_type': 'category',
        'all_categories': all_categories,
        'all_industries': all_industries,
        'meta_title': category.meta_title or f"{category.name} Adhesives & Sealants | Uniworld",
        'meta_description': category.meta_description or f"Explore Uniworld {category.name.lower()} adhesives, sealants and primers manufactured in Bangladesh for industrial and commercial use.",
    }
    return render(request, 'product.html', context)


def industries_hub(request):
    """Overview hub of all industries served by Uniworld."""
    industries = Industry.objects.filter(parent=None, is_active=True).prefetch_related('subindustries', 'products')
    context = {
        'industries': industries,
        'meta_title': 'Industries We Serve: Footwear, Furniture & Hardware | Uniworld',
        'meta_description': 'Industrial bonding and sealing solutions tailored for footwear manufacturing, furniture & foam lamination, construction, automotive and hardware retail in Bangladesh.',
    }
    return render(request, 'industries.html', context)


def industry_products(request, slug):
    """Industry products page."""
    if any(c.isupper() for c in slug):
        return redirect('industry_products', slug=slug.lower(), permanent=True)

    industry = get_object_or_404(Industry, slug__iexact=slug, is_active=True)

    industry_ids = [industry.pk]
    for subindustry in industry.subindustries.filter(is_active=True):
        industry_ids.append(subindustry.pk)

    products = Product.objects.filter(industry__pk__in=industry_ids).select_related('category', 'industry').prefetch_related('images')
    all_categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('subcategories')
    all_industries = Industry.objects.filter(parent=None, is_active=True).prefetch_related('subindustries')

    context = {
        'products': products,
        'industry': industry,
        'filter_type': 'industry',
        'all_categories': all_categories,
        'all_industries': all_industries,
        'meta_title': industry.meta_title or f"{industry.name} Adhesives & Bonding Solutions | Uniworld",
        'meta_description': industry.meta_description or f"High-performance adhesives and sealants formulated for the {industry.name.lower()} sector in Bangladesh.",
    }
    return render(request, 'product.html', context)


def blog_list(request):
    """Blog listing page - noindex until at least 3 posts are live."""
    posts = Blog.objects.filter(is_published=True).order_by('-published_date')
    context = {
        'posts': posts,
        'noindex': posts.count() < 3,
        'meta_title': 'Adhesive & Sealant Guides and News | Uniworld Blog',
        'meta_description': 'Practical guides to choosing and applying adhesives, sealants and primers for footwear, furniture and construction, plus Uniworld product news and updates.',
    }
    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    """Blog detail page."""
    post = get_object_or_404(Blog, slug=slug, is_published=True)
    related_posts = Blog.objects.filter(is_published=True).exclude(uuid=post.uuid)[:3]
    context = {
        'post': post,
        'related_posts': related_posts,
        'meta_title': post.meta_title or f"{post.title} | Uniworld Blog",
        'meta_description': post.meta_description or post.excerpt[:158],
    }
    return render(request, 'blog_details.html', context)


def about(request):
    """About page."""
    context = {
        'meta_title': 'About Uniworld Adhesives & Sealants | Since 2018',
        'meta_description': 'Founded in 2018, Uniworld makes ISO 9001:2015 certified adhesives and sealants at its Rupganj factory for footwear, furniture, construction and manufacturing.',
    }
    return render(request, 'about.html', context)


def contact(request):
    """Contact page."""
    context = {
        'meta_title': 'Contact Uniworld Adhesives | Request a Quote',
        'meta_description': 'Request a quote or technical advice. Head office: Family World Tower, Asad Gate, Dhaka 1207. Factory: Rupganj, Narayanganj. Call +880 1898-802405.',
    }
    return render(request, 'contact.html', context)


def sustainability(request):
    """Sustainability page."""
    context = {
        'meta_title': 'Sustainability in Adhesive Manufacturing | Uniworld',
        'meta_description': 'How Uniworld reduces environmental impact through greener chemistry, cleaner production and responsible adhesive manufacturing at its Bangladesh factory.',
    }
    return render(request, 'sustainability.html', context)


def rnd(request):
    """Research & Development and Quality Control page."""
    context = {
        'meta_title': 'Adhesive R&D and Quality Testing | Uniworld',
        'meta_description': 'How Uniworld develops and tests adhesives: formulation and material analysis, peel, shear and tack tests, heat and chemical resistance, and substrate trials.',
    }
    return render(request, 'r&d.html', context)


def faq_page(request):
    """B2B Ordering, MOQ, Delivery & Technical Support FAQ page."""
    context = {
        'meta_title': 'Frequently Asked Questions: Ordering, MOQ & Delivery | Uniworld',
        'meta_description': 'Answers to common B2B questions about minimum order quantities (MOQ), bulk packaging, nationwide delivery in Bangladesh, and custom adhesive formulation.',
    }
    return render(request, 'faq.html', context)


def privacy_policy(request):
    """Privacy Policy page."""
    context = {
        'meta_title': 'Privacy Policy | Uniworld Adhesives',
        'meta_description': 'Read how Uniworld Adhesives collects, uses, and protects your business inquiry and contact information.',
    }
    return render(request, 'privacy_policy.html', context)


def terms_of_use(request):
    """Terms of Use page."""
    context = {
        'meta_title': 'Terms of Use | Uniworld Adhesives',
        'meta_description': 'Terms and conditions governing the use of the Uniworld Adhesives website, technical data sheets, and product inquiries.',
    }
    return render(request, 'terms_of_use.html', context)


def downloads(request):
    """Downloads page."""
    download_categories = DownloadCategory.objects.filter(is_active=True).prefetch_related('files')
    products_with_docs = Product.objects.exclude(tds_file='', sds_file='').prefetch_related('images')
    context = {
        'download_categories': download_categories,
        'products_with_docs': products_with_docs,
        'meta_title': 'Product Catalogue & Company Profile (PDF) | Uniworld',
        'meta_description': 'Download the Uniworld product catalogue and 2026 company profile as PDF files to share with your purchasing, production or technical team.',
    }
    return render(request, 'downloads.html', context)


def download_file_by_slug(request, slug):
    """Serve PDF cleanly via SEO-friendly URL (/downloads/uniworld-product-catalogue-2026.pdf)."""
    doc = get_object_or_404(DownloadFile, slug=slug, is_active=True)
    try:
        response = FileResponse(doc.file.open('rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{slug}.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("File not found")


def download_file(request, uuid):
    """Legacy UUID download route - redirects to slug URL if available, else serves file."""
    doc = get_object_or_404(DownloadFile, uuid=uuid, is_active=True)
    if doc.slug:
        return redirect('download_file_slug', slug=doc.slug, permanent=True)
    try:
        return FileResponse(doc.file.open('rb'), as_attachment=True)
    except FileNotFoundError:
        raise Http404("File not found")