"""
Views for handling inquiry submissions (product quotes and contact forms).
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import get_connection, EmailMessage

from .models import Product, Inquiry, EmailConfiguration


def send_inquiry_notification(inquiry):
    """Send email notification for new inquiry."""
    config = EmailConfiguration.objects.filter(is_active=True).first()
    if not config:
        return False
    
    try:
        subject = f"New {'Product Quote' if inquiry.product else 'Contact'} Request - {inquiry.full_name}"
        
        body = f"""
New inquiry received:

Type: {inquiry.inquiry_type}
{'Product: ' + inquiry.product.name if inquiry.product else ''}
{'Selected Sizes: ' + inquiry.selected_sizes if inquiry.selected_sizes else ''}

Customer Details:
Name: {inquiry.full_name}
Email: {inquiry.email}
Phone: {inquiry.phone}

Message:
{inquiry.message}

Received at: {inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        connection = get_connection(
            host=config.smtp_host,
            port=config.smtp_port,
            username=config.smtp_username,
            password=config.smtp_password,
            use_tls=config.use_tls,
            use_ssl=config.use_ssl
        )
        
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=config.smtp_username,
            to=config.get_recipient_list(),
            connection=connection
        )
        email.send()
        return True
    except Exception:
        return False


@require_POST
def submit_inquiry(request):
    """Handle inquiry form submissions (product quotes and contact forms)."""
    try:
        data = json.loads(request.body)
        
        # Validation
        errors = {}
        if not data.get('full_name', '').strip():
            errors['full_name'] = 'Full name is required'
        
        email_value = data.get('email', '').strip()
        if not email_value:
            errors['email'] = 'Email is required'
        else:
            try:
                validate_email(email_value)
            except ValidationError:
                errors['email'] = 'Invalid email format'
        
        if not data.get('phone', '').strip():
            errors['phone'] = 'Phone number is required'
        
        if not data.get('message', '').strip():
            errors['message'] = 'Message is required'
        
        # Size validation for product quotes
        product_uuid = data.get('product_uuid')
        product = None
        if product_uuid:
            product = Product.objects.filter(uuid=product_uuid).first()
            if product and product.sizes and not data.get('selected_sizes'):
                errors['sizes'] = 'Please select at least one size'
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
        # Create inquiry
        inquiry = Inquiry.objects.create(
            product=product,
            selected_sizes=data.get('selected_sizes', ''),
            full_name=data['full_name'].strip(),
            email=email_value,
            phone=data['phone'].strip(),
            message=data['message'].strip()
        )
        
        # Send email notification (don't fail if email fails)
        send_inquiry_notification(inquiry)
        
        return JsonResponse({
            'success': True,
            'message': "We received your request. We'll get back to you by email"
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
