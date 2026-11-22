import uuid
import re
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Industry(models.Model):
    """Industry model with self-referencing parent field for nested hierarchies."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subindustries'
    )
    feature_image = models.ImageField(upload_to='industries/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True, help_text="Descriptive alt text for SEO")
    content = RichTextUploadingField(blank=True)
    
    # SEO & Content Expansion Fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=165, blank=True)
    h1_title = models.CharField(max_length=200, blank=True)
    faqs = models.JSONField(default=list, blank=True, help_text='List of {"question": "...", "answer": "..."}')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Industries'

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_children(self):
        return self.subindustries.filter(is_active=True)


class Category(models.Model):
    """Category model with self-referencing parent field for nested hierarchies."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    feature_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True)
    content = RichTextUploadingField(blank=True)
    
    # SEO & Content Expansion Fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=165, blank=True)
    h1_title = models.CharField(max_length=200, blank=True)
    buying_guide = RichTextUploadingField(blank=True, help_text="How to choose the right adhesive guide")
    faqs = models.JSONField(default=list, blank=True, help_text='List of {"question": "...", "answer": "..."}')
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Categories'

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_children(self):
        return self.subcategories.filter(is_active=True)


class Product(models.Model):
    """Product model with full SEO, Technical Specifications, and FAQ support."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=165, blank=True)
    h1_title = models.CharField(max_length=200, blank=True)
    
    # Structured Content Sections (300-500 words target)
    short_tagline = models.CharField(max_length=255, blank=True, help_text="e.g., High-tack solvent adhesive for EVA & rubber")
    description = models.TextField(help_text="What is {product}? 2-3 sentence keyword-rich intro")
    features = models.TextField(blank=True, help_text="One feature per line")
    applications = models.TextField(blank=True, help_text="Industries and suitable substrates")
    how_to_apply = models.TextField(blank=True, help_text="Numbered application steps including surface prep")
    sizes = models.TextField(blank=True, help_text="Pack sizes e.g., 3 L, 15 L, 300 ml")
    
    # Engineering & Technical Data (for Spec Tables & Charts)
    tech_specs = models.JSONField(
        default=dict,
        blank=True,
        help_text='e.g. {"Base": "SBS", "Colour": "Clear/Amber", "Viscosity": "80-120 cPs", "Open Time": "2-5 min", "Cure Time": "24 hrs", "Temp Range": "-10°C to 70°C", "Shelf Life": "12 Months"}'
    )
    viscosity_min = models.PositiveIntegerField(null=True, blank=True, help_text="For comparison charts (cPs)")
    viscosity_max = models.PositiveIntegerField(null=True, blank=True, help_text="For comparison charts (cPs)")
    peel_strength = models.CharField(max_length=100, blank=True, help_text="e.g., 4.5 N/mm")
    
    # FAQs for Product Page & FAQPage Schema
    faqs = models.JSONField(
        default=list,
        blank=True,
        help_text='List of {"question": "...", "answer": "..."}'
    )
    
    # Technical Documents (B2B Downloads)
    tds_file = models.FileField(upload_to='tds/', blank=True, null=True, verbose_name="Technical Data Sheet (TDS)")
    sds_file = models.FileField(upload_to='sds/', blank=True, null=True, verbose_name="Safety Data Sheet (SDS)")
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    related_products_manual = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        help_text="Select companion primers, cleaners, or alternative grades"
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        # Automatically strip hidden U+2060 word-joiner or zero-width characters
        if self.name:
            self.name = re.sub(r'[\u200b-\u200d\u2060\ufeff]', '', self.name).strip()
        if self.h1_title:
            self.h1_title = re.sub(r'[\u200b-\u200d\u2060\ufeff]', '', self.h1_title).strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def display_h1(self):
        return self.h1_title or self.name

    @property
    def display_meta_title(self):
        return self.meta_title or f"{self.name} | Uniworld"

    @property
    def feature_image(self):
        first_image = self.images.filter(is_primary=True).first() or self.images.first()
        return first_image if first_image else None

    def get_features_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    def get_steps_list(self):
        return [line.strip() for line in self.how_to_apply.splitlines() if line.strip()]

    def get_sizes_list(self):
        if not self.sizes:
            return []
        # Supports both newline-separated and comma-separated sizes
        raw_items = re.split(r'[\r\n,]+', self.sizes)
        return [s.strip() for s in raw_items if s.strip()]


class ProductImage(models.Model):
    """Model for storing multiple images per product with SEO alt text."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"

    @property
    def src(self):
        """Returns static URL if path starts with product/, else standard media URL."""
        if not self.image:
            return '/static/product/images/product/01.png'
        name = str(self.image.name)
        if name.startswith('product/'):
            return f'/static/{name}'
        return self.image.url

    @property
    def get_alt(self):
        return self.alt_text or f"{self.product.name} - Uniworld Adhesives Bangladesh"


class Blog(models.Model):
    """Blog model with publishing and SEO features."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=165, blank=True)
    content = RichTextUploadingField()
    excerpt = models.TextField(max_length=500, blank=True)
    author = models.CharField(max_length=100, default='Uniworld Technical Team')
    featured_image = models.ImageField(upload_to='blogs/')
    image_alt = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title


class Contact(models.Model):
    """Contact model for single source of truth NAP (Name, Address, Phone, Hours)."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=200, default="Uniworld Adhesives")
    factory_address = models.TextField()
    head_office_address = models.TextField()
    phone = models.CharField(max_length=50)
    phone_2 = models.CharField(max_length=50, blank=True)
    phone_3 = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    working_hours = models.CharField(max_length=200)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Information'

    def __str__(self):
        return self.company_name


class Inquiry(models.Model):
    """Model for storing product quote requests and general contact inquiries."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries'
    )
    selected_sizes = models.TextField(blank=True)
    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        if self.product:
            return f"Quote: {self.product.name} - {self.full_name}"
        return f"Contact: {self.full_name}"

    @property
    def inquiry_type(self):
        return "Product Quote" if self.product else "General Inquiry"


class EmailConfiguration(models.Model):
    """Model for storing SMTP settings and recipient emails for inquiry notifications."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    smtp_host = models.CharField(max_length=255)
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_username = models.CharField(max_length=255)
    smtp_password = models.CharField(max_length=255)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    email_1 = models.EmailField()
    email_2 = models.EmailField(blank=True)
    email_3 = models.EmailField(blank=True)
    email_4 = models.EmailField(blank=True)
    email_5 = models.EmailField(blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Email Configurations'

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.smtp_host} ({status})"

    def save(self, *args, **kwargs):
        if self.is_active:
            EmailConfiguration.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def get_recipient_list(self):
        return [e for e in [self.email_1, self.email_2, self.email_3, self.email_4, self.email_5] if e]


class DownloadCategory(models.Model):
    """Category model for organizing downloadable files."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name_plural = 'Download Categories'

    def __str__(self):
        return self.title


class DownloadFile(models.Model):
    """Model for storing downloadable files with SEO-friendly slugs."""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        DownloadCategory,
        on_delete=models.CASCADE,
        related_name='files'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="e.g. uniworld-product-catalogue-2026")
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='downloads/')
    file_size = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name_plural = 'Download Files'

    def __str__(self):
        return f"{self.title} ({self.category.title})"

    def get_file_extension(self):
        if self.file:
            return self.file.name.split('.')[-1].upper()
        return ''

    def get_file_size_display(self):
        if self.file_size:
            return self.file_size
        if self.file:
            try:
                size_bytes = self.file.size
                if size_bytes < 1024:
                    return f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    return f"{size_bytes / 1024:.1f} KB"
                else:
                    return f"{size_bytes / (1024 * 1024):.1f} MB"
            except Exception:
                return ''
        return ''