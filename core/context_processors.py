import urllib.parse
from datetime import datetime
from .models import SiteSettings, Service

def site_context(request):
    """
    Site-wide context processor providing settings, navigation items,
    and dynamic contact/WhatsApp helpers across all templates.
    """
    try:
        settings_obj = SiteSettings.load()
    except Exception:
        settings_obj = None

    phone = getattr(settings_obj, 'phone', '+254713706103') if settings_obj else '+254713706103'
    clean_phone = phone.replace(' ', '').replace('-', '')
    whatsapp_num = getattr(settings_obj, 'whatsapp_number', '254713706103') if settings_obj else '254713706103'
    clean_whatsapp = whatsapp_num.replace('+', '').replace(' ', '').replace('-', '')

    # Pre-encoded default WhatsApp message
    default_msg = "Hello Gen-Z Constructors Limited Company, I would like to enquire about your construction services."
    encoded_default_msg = urllib.parse.quote(default_msg)
    whatsapp_default_url = f"https://wa.me/{clean_whatsapp}?text={encoded_default_msg}"

    quote_msg = "Hello Gen-Z Constructors Limited Company, I would like to request a quotation for my project."
    encoded_quote_msg = urllib.parse.quote(quote_msg)
    whatsapp_quote_url = f"https://wa.me/{clean_whatsapp}?text={encoded_quote_msg}"

    # Navigation services (cached or ordered)
    try:
        nav_services = Service.objects.all().order_by('display_order', 'name')[:8]
    except Exception:
        nav_services = []

    return {
        'site_settings': settings_obj,
        'nav_services': nav_services,
        'current_year': datetime.now().year,
        'company_phone_clean': clean_phone,
        'company_phone_display': phone,
        'company_whatsapp_num': clean_whatsapp,
        'whatsapp_default_url': whatsapp_default_url,
        'whatsapp_quote_url': whatsapp_quote_url,
        'company_email': getattr(settings_obj, 'email', 'genzconstructors@gmail.com') if settings_obj else 'genzconstructors@gmail.com',
        'company_domain': getattr(settings_obj, 'website', 'genzconstructors.co.ke') if settings_obj else 'genzconstructors.co.ke',
    }
