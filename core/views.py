import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    SiteSettings, Service, Project, ProcessStep,
    Testimonial, FAQ, Enquiry, ContactMessage
)
from .forms import QuoteRequestForm, ContactForm


def home(request):
    """
    Homepage - Central landing page with high-conversion structure.
    """
    services = Service.objects.all().order_by('display_order', 'name')
    featured_services = services[:6]
    process_steps = ProcessStep.objects.filter(active=True).order_by('step_number')[:7]
    featured_projects = Project.objects.filter(featured=True).prefetch_related('services')[:6]
    if not featured_projects.exists():
        featured_projects = Project.objects.all().prefetch_related('services')[:6]
    testimonials = Testimonial.objects.filter(featured=True).order_by('-rating', '-created_at')[:6]
    faqs = FAQ.objects.filter(active=True).order_by('display_order')[:6]

    context = {
        'services': services,
        'featured_services': featured_services,
        'process_steps': process_steps,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
        'faqs': faqs,
        'meta_title': 'Gen-Z Constructors Limited Company | Building Your Vision, Constructing Your Future',
        'meta_description': 'Professional construction, architectural design, structural engineering, renovations and modern building solutions across Kenya.',
    }
    return render(request, 'home/index.html', context)


def about(request):
    """
    About Us - Company background, core values, architectural philosophy.
    """
    services = Service.objects.all()[:4]
    process_steps = ProcessStep.objects.filter(active=True).order_by('step_number')[:4]
    testimonials = Testimonial.objects.filter(featured=True)[:3]

    context = {
        'services': services,
        'process_steps': process_steps,
        'testimonials': testimonials,
        'meta_title': 'About Gen-Z Constructors Limited Company | Modern Building Solutions',
        'meta_description': 'Discover our client-focused approach, commitment to structural integrity, and modern construction practices designed for tomorrow.',
    }
    return render(request, 'about/index.html', context)


def services_list(request):
    """
    Services catalog - Comprehensive breakdown of construction solutions.
    """
    all_services = Service.objects.all().order_by('display_order', 'name')
    categories = Service.CATEGORY_CHOICES

    # Optional filter by category
    selected_cat = request.GET.get('category', '').strip()
    if selected_cat:
        services = all_services.filter(category=selected_cat)
    else:
        services = all_services

    context = {
        'services': services,
        'all_services': all_services,
        'categories': categories,
        'selected_category': selected_cat,
        'meta_title': 'Construction & Building Services | Gen-Z Constructors',
        'meta_description': 'Explore our complete range of building construction, architectural design, structural solutions, renovations and landscaping services in Kenya.',
    }
    return render(request, 'services/index.html', context)


def service_detail(request, slug):
    """
    Individual service detail page.
    """
    service = get_object_or_404(Service, slug=slug)
    related_projects = Project.objects.filter(services=service)[:4]
    other_services = Service.objects.exclude(id=service.id).order_by('display_order')[:4]
    process_steps = ProcessStep.objects.filter(active=True).order_by('step_number')[:4]

    # Pre-encoded WhatsApp message specific to this service
    settings_obj = SiteSettings.load()
    whatsapp_num = getattr(settings_obj, 'whatsapp_number', '254713706103').replace('+', '').replace(' ', '')
    service_msg = f"Hello Gen-Z Constructors Limited Company, I am interested in your {service.name}. Please share more information."
    service_whatsapp_url = f"https://wa.me/{whatsapp_num}?text={urllib.parse.quote(service_msg)}"

    context = {
        'service': service,
        'related_projects': related_projects,
        'other_services': other_services,
        'process_steps': process_steps,
        'service_whatsapp_url': service_whatsapp_url,
        'meta_title': service.seo_title or f"{service.name} | Gen-Z Constructors",
        'meta_description': service.seo_description or service.short_description,
    }
    return render(request, 'services/detail.html', context)


def projects_list(request):
    """
    Portfolio projects gallery with category filters and pagination.
    """
    category_filter = request.GET.get('category', '').strip()
    status_filter = request.GET.get('status', '').strip()

    projects_qs = Project.objects.all().prefetch_related('services')

    if category_filter:
        projects_qs = projects_qs.filter(category=category_filter)
    if status_filter:
        projects_qs = projects_qs.filter(status=status_filter)

    paginator = Paginator(projects_qs, 9)
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)

    context = {
        'projects': projects_page,
        'categories': Project.CATEGORY_CHOICES,
        'statuses': Project.STATUS_CHOICES,
        'selected_category': category_filter,
        'selected_status': status_filter,
        'meta_title': 'Projects Portfolio | Gen-Z Constructors Limited Company',
        'meta_description': 'Explore our featured construction, architectural and renovation projects. See craftsmanship, design and structural quality in action.',
    }
    return render(request, 'projects/index.html', context)


def project_detail(request, slug):
    """
    Detailed project showcase with gallery images.
    """
    project = get_object_or_404(Project.objects.prefetch_related('gallery_images', 'services'), slug=slug)
    related_projects = Project.objects.filter(category=project.category).exclude(id=project.id)[:3]
    if not related_projects.exists():
        related_projects = Project.objects.exclude(id=project.id)[:3]

    # Pre-encoded WhatsApp message specific to this project
    settings_obj = SiteSettings.load()
    whatsapp_num = getattr(settings_obj, 'whatsapp_number', '254713706103').replace('+', '').replace(' ', '')
    project_msg = f"Hello Gen-Z Constructors Limited Company, I would like to discuss a project similar to '{project.title}' that I saw on your website."
    project_whatsapp_url = f"https://wa.me/{whatsapp_num}?text={urllib.parse.quote(project_msg)}"

    context = {
        'project': project,
        'gallery': project.gallery_images.all(),
        'related_projects': related_projects,
        'project_whatsapp_url': project_whatsapp_url,
        'meta_title': project.seo_title or f"{project.title} | Gen-Z Constructors Portfolio",
        'meta_description': project.seo_description or project.short_description,
    }
    return render(request, 'projects/detail.html', context)


def process_view(request):
    """
    Our 7-Step Construction Process.
    """
    steps = ProcessStep.objects.filter(active=True).order_by('step_number')
    faqs = FAQ.objects.filter(active=True)[:4]

    context = {
        'steps': steps,
        'faqs': faqs,
        'meta_title': 'Our Construction Process | Gen-Z Constructors',
        'meta_description': 'Discover our transparent, 7-step construction workflow from initial consultation to final inspection and handover.',
    }
    return render(request, 'process/index.html', context)


def request_quote(request):
    """
    Request a Quote lead generation form.
    """
    service_slug = request.GET.get('service', '').strip()
    initial_data = {}
    if service_slug:
        try:
            matched_service = Service.objects.get(slug=service_slug)
            initial_data['service'] = matched_service
        except Service.DoesNotExist:
            pass

    if request.method == 'POST':
        form = QuoteRequestForm(request.POST, request.FILES)
        if form.is_valid():
            enquiry = form.save()

            # Optional email notification
            try:
                subject = f"[New Quote Enquiry #{enquiry.id}] {enquiry.full_name} - {enquiry.get_project_type_display()}"
                body = (
                    f"New Project Quote Request Received:\n\n"
                    f"Name: {enquiry.full_name}\n"
                    f"Phone: {enquiry.phone}\n"
                    f"Email: {enquiry.email}\n"
                    f"Location: {enquiry.location}\n"
                    f"Project Type: {enquiry.get_project_type_display()}\n"
                    f"Service: {enquiry.service.name if enquiry.service else 'N/A'}\n"
                    f"Budget: {enquiry.get_budget_display()}\n"
                    f"Timeline: {enquiry.get_preferred_start_date_display()}\n"
                    f"Details:\n{enquiry.description}\n"
                )
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.COMPANY_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                "Thank you! Your project enquiry has been received. Our team will review your requirements and get in touch promptly."
            )
            return redirect('core:quote_success', pk=enquiry.id)
        else:
            messages.error(request, "Please review the form below and correct any highlighted errors.")
    else:
        form = QuoteRequestForm(initial=initial_data)

    context = {
        'form': form,
        'meta_title': 'Request a Quotation | Gen-Z Constructors Limited Company',
        'meta_description': 'Get a free, detailed quotation for your building, design or renovation project from Gen-Z Constructors. Transparent pricing and expert consultation.',
    }
    return render(request, 'quote/index.html', context)


def quote_success(request, pk):
    """
    Confirmation screen after quotation submission with direct WhatsApp link.
    """
    enquiry = get_object_or_404(Enquiry, pk=pk)
    settings_obj = SiteSettings.load()
    whatsapp_num = getattr(settings_obj, 'whatsapp_number', '254713706103').replace('+', '').replace(' ', '')

    # Prepare detailed WhatsApp continuation message
    quote_summary_msg = (
        f"Hello Gen-Z Constructors, I just submitted Quote Request #{enquiry.id} on your website.\n\n"
        f"Name: {enquiry.full_name}\n"
        f"Project: {enquiry.get_project_type_display()}\n"
        f"Location: {enquiry.location or 'Not specified'}\n"
        f"I would like to follow up directly."
    )
    direct_whatsapp_url = f"https://wa.me/{whatsapp_num}?text={urllib.parse.quote(quote_summary_msg)}"

    context = {
        'enquiry': enquiry,
        'direct_whatsapp_url': direct_whatsapp_url,
        'meta_title': 'Enquiry Received | Gen-Z Constructors',
        'meta_description': 'Your project quotation request has been received by Gen-Z Constructors.',
    }
    return render(request, 'quote/success.html', context)


def contact_view(request):
    """
    Contact Us page with interactive form, phone, WhatsApp and email details.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()

            # Optional email notification
            try:
                send_mail(
                    subject=f"[Website Contact] {contact_msg.subject} from {contact_msg.full_name}",
                    message=f"From: {contact_msg.full_name} <{contact_msg.email}>\nPhone: {contact_msg.phone}\n\nMessage:\n{contact_msg.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.COMPANY_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                "Thank you for contacting Gen-Z Constructors! Your message has been received and our team will get back to you shortly."
            )
            return redirect('core:contact')
        else:
            messages.error(request, "Please check the contact form for any missing or invalid details.")
    else:
        form = ContactForm()

    context = {
        'form': form,
        'meta_title': 'Contact Us | Gen-Z Constructors Limited Company',
        'meta_description': 'Get in touch with Gen-Z Constructors. Call +254 713 706 103, chat on WhatsApp, or send us a message to discuss your next construction project.',
    }
    return render(request, 'contact/index.html', context)


def robots_txt(request):
    """
    Dynamic robots.txt response.
    """
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Disallow: /quote/success/\n\n"
        f"Sitemap: https://{settings.COMPANY_DOMAIN}/sitemap.xml\n"
    )
    return HttpResponse(content, content_type="text/plain")


def custom_404(request, exception):
    """
    Branded 404 Error page.
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Branded 500 Error page.
    """
    return render(request, '500.html', status=500)


def custom_403(request, exception):
    """
    Branded 403 Error page.
    """
    return render(request, '403.html', status=403)
