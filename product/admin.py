from django.contrib import admin
from django.utils.text import slugify
from unfold.admin import ModelAdmin, TabularInline
from .models import Industry, Category, Product, ProductImage, Blog, Contact, Inquiry, EmailConfiguration, DownloadCategory, DownloadFile


class ProductImageInline(TabularInline):
    """Inline admin for managing multiple product images."""
    model = ProductImage
    extra = 1
    ordering = ['order']
    fields = ['image', 'is_primary', 'order']
    tab = True


@admin.register(Industry)
class IndustryAdmin(ModelAdmin):
    """Admin configuration for Industry model with Unfold theme."""
    list_display = ('name', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter_submit = True
    list_display_links = ('name',)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """Admin configuration for Category model with Unfold theme."""
    list_display = ('name', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter_submit = True
    list_display_links = ('name',)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Admin configuration for Product model with Unfold theme and image inline."""
    list_display = ('name', 'category', 'industry', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'category', 'industry', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    list_filter_submit = True
    list_display_links = ('name',)

    def save_model(self, request, obj, form, change):
        """Auto-generate slug from name if not provided."""
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    """Admin configuration for Blog model with Unfold theme."""
    list_display = ('title', 'author', 'is_published', 'published_date')
    list_filter = ('is_published', 'published_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_filter_submit = True
    list_display_links = ('title',)

    def save_model(self, request, obj, form, change):
        """Auto-generate slug from title if not provided."""
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    """Admin configuration for Contact model with Unfold theme."""
    list_display = ('company_name', 'phone', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('company_name', 'phone', 'email')


@admin.register(Inquiry)
class InquiryAdmin(ModelAdmin):
    """Admin configuration for Inquiry model with Unfold theme."""
    list_display = ('get_product_name', 'full_name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'product')
    search_fields = ('full_name', 'email', 'product__name')
    readonly_fields = ('uuid', 'created_at')
    list_filter_submit = True
    list_display_links = ('get_product_name', 'full_name')
    actions = ['mark_as_read', 'mark_as_unread']

    def get_product_name(self, obj):
        """Display product name or 'General Inquiry' for contact submissions."""
        return obj.product.name if obj.product else "General Inquiry"
    get_product_name.short_description = 'Product/Type'
    get_product_name.admin_order_field = 'product__name'

    @admin.action(description='Mark selected inquiries as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description='Mark selected inquiries as unread')
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(EmailConfiguration)
class EmailConfigurationAdmin(ModelAdmin):
    """Admin configuration for EmailConfiguration model with Unfold theme."""
    list_display = ('smtp_host', 'smtp_port', 'smtp_username', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('smtp_host', 'smtp_username')
    readonly_fields = ('uuid', 'created_at')
    list_filter_submit = True
    fieldsets = (
        ('SMTP Settings', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'use_tls', 'use_ssl')
        }),
        ('Recipient Emails', {
            'fields': ('email_1', 'email_2', 'email_3', 'email_4', 'email_5')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Info', {
            'fields': ('uuid', 'created_at'),
            'classes': ('collapse',)
        }),
    )


class DownloadFileInline(TabularInline):
    """Inline admin for managing files within a category."""
    model = DownloadFile
    extra = 1
    ordering = ['order']
    fields = ['title', 'description', 'file', 'file_size', 'order', 'is_active']
    tab = True


@admin.register(DownloadCategory)
class DownloadCategoryAdmin(ModelAdmin):
    """Admin configuration for DownloadCategory model with Unfold theme."""
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    inlines = [DownloadFileInline]
    list_filter_submit = True
    list_display_links = ('title',)


@admin.register(DownloadFile)
class DownloadFileAdmin(ModelAdmin):
    """Admin configuration for DownloadFile model with Unfold theme."""
    list_display = ('title', 'category', 'get_file_extension', 'get_file_size_display', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    list_filter_submit = True
    list_display_links = ('title',)
