from .models import Contact, Category, Industry


def base_context(request):
    """
    Context processor to provide data needed by all templates.
    This makes contact_info, categories, and industries available in all templates.
    """
    # Get active contact information for footer
    contact_info = Contact.objects.filter(is_active=True).first()

    # Get top-level active categories for Product dropdown navigation (parent=None for hierarchy)
    categories = Category.objects.filter(
        parent=None,
        is_active=True
    ).prefetch_related('subcategories', 'products')

    # Get top-level active industries for Industry dropdown navigation
    industries = Industry.objects.filter(
        parent=None,
        is_active=True
    ).prefetch_related('subindustries', 'products')

    return {
        'contact_info': contact_info,
        'categories': categories,
        'industries': industries,
    }
