import os
import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed formats: {", ".join(valid_extensions)}')
    # 10MB limit
    if value.size > 10 * 1024 * 1024:
        raise ValidationError('File size must be under 10MB.')

def safe_attachment_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    clean_name = f"{uuid.uuid4().hex[:12]}{ext}"
    return f"enquiry_attachments/{clean_name}"


class SiteSettings(models.Model):
    """
    Singleton model for global website configuration, contact information,
    brand assets and social media links.
    """
    business_name = models.CharField(
        max_length=200,
        default="Gen-Z Constructors Limited Company"
    )
    tagline = models.CharField(
        max_length=255,
        default="BUILDING YOUR VISION, CONSTRUCTING YOUR FUTURE."
    )
    phone = models.CharField(max_length=50, default="+254713706103")
    email = models.EmailField(default="genzconstructors@gmail.com")
    website = models.CharField(max_length=100, default="genzconstructors.co.ke")
    whatsapp_number = models.CharField(
        max_length=50,
        default="254713706103",
        help_text="Phone number format for WhatsApp API without + or spaces (e.g. 254713706103)"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Only enter verified physical operating location"
    )
    business_hours = models.CharField(
        max_length=150,
        blank=True,
        default="Mon - Fri: 8:00 AM - 5:00 PM | Sat: 8:00 AM - 1:00 PM"
    )
    facebook_url = models.URLField(
        blank=True,
        help_text="Official Facebook page URL"
    )
    instagram_url = models.URLField(
        blank=True,
        help_text="Official Instagram profile URL"
    )
    logo = models.ImageField(
        upload_to='branding/',
        blank=True,
        null=True,
        help_text="Official brand logo"
    )
    favicon = models.ImageField(
        upload_to='branding/',
        blank=True,
        null=True,
        help_text="Favicon icon"
    )
    default_meta_title = models.CharField(
        max_length=255,
        default="Gen-Z Constructors Limited Company | Construction & Building Solutions"
    )
    default_meta_description = models.TextField(
        default="Gen-Z Constructors Limited Company delivers modern construction, architectural design, structural engineering, renovations and building solutions across Kenya. Building Your Vision, Constructing Your Future."
    )
    map_embed_url = models.TextField(
        blank=True,
        help_text="Google Maps iframe URL or embed code (optional)"
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        # Enforce singleton
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    """
    Construction solutions and services offered by Gen-Z Constructors.
    """
    CATEGORY_CHOICES = [
        ('construction', 'Building & Construction'),
        ('design', 'Architectural & Engineering'),
        ('specialized', 'Specialized Building Solutions'),
        ('renovation', 'Renovation & Maintenance'),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='construction')
    short_description = models.CharField(
        max_length=255,
        help_text="Concise summary for cards and search results"
    )
    description = models.TextField(
        help_text="Detailed description of what the service involves, process, and benefits"
    )
    key_features = models.TextField(
        blank=True,
        help_text="Comma-separated or bullet points of key highlights and deliverables"
    )
    icon = models.CharField(
        max_length=50,
        default="building-2",
        help_text="Lucide icon name (e.g. building-2, pen-tool, hard-hat, hammer, wrench, compass, trees, droplet)"
    )
    featured_image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True
    )
    featured = models.BooleanField(
        default=False,
        help_text="Display prominently on homepage"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lowest numbers appear first"
    )
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.seo_title:
            self.seo_title = f"{self.name} | Gen-Z Constructors Limited Company"
        if not self.seo_description:
            self.seo_description = self.short_description
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:service_detail', kwargs={'slug': self.slug})

    def get_features_list(self):
        if not self.key_features:
            return []
        return [f.strip() for f in self.key_features.split('\n') if f.strip()]


class Project(models.Model):
    """
    Project portfolio showcase.
    """
    CATEGORY_CHOICES = [
        ('residential', 'Residential Construction'),
        ('commercial', 'Commercial Construction'),
        ('architectural', 'Architectural Design'),
        ('structural', 'Structural Solutions'),
        ('renovation', 'Renovation & Remodeling'),
        ('landscaping', 'Landscaping & Outdoors'),
        ('specialized', 'Specialized Solutions'),
    ]

    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('planned', 'Planned'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='residential')
    location = models.CharField(max_length=150, blank=True, help_text="e.g. Mombasa, Nairobi, Coastal Region")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    scope_of_work = models.TextField(
        blank=True,
        help_text="Key highlights or work items undertaken on this project"
    )
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    services = models.ManyToManyField(
        Service,
        related_name='projects',
        blank=True
    )
    featured = models.BooleanField(default=False, help_text="Display on Homepage showcase")
    is_sample = models.BooleanField(
        default=False,
        help_text="Label as sample project until actual project photos are uploaded"
    )
    display_order = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.seo_title:
            self.seo_title = f"{self.title} | Gen-Z Constructors Projects"
        if not self.seo_description:
            self.seo_description = self.short_description
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'slug': self.slug})

    def get_scope_list(self):
        if not self.scope_of_work:
            return []
        return [s.strip() for s in self.scope_of_work.split('\n') if s.strip()]


class ProjectImage(models.Model):
    """
    Additional gallery photos for a Project.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "Project Gallery Image"
        verbose_name_plural = "Project Gallery Images"

    def __str__(self):
        return f"{self.project.title} - Image #{self.id}"


class ProcessStep(models.Model):
    """
    Step in the 7-step construction methodology.
    """
    step_number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        default="check-circle",
        help_text="Lucide icon name"
    )
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['step_number', 'display_order']
        verbose_name = "Process Step"
        verbose_name_plural = "Process Steps"

    def __str__(self):
        return f"{self.step_number:02d}. {self.title}"


class Testimonial(models.Model):
    """
    Client testimonials and reviews.
    """
    client_name = models.CharField(max_length=150)
    role_or_company = models.CharField(
        max_length=150,
        blank=True,
        help_text="e.g. Homeowner, Nyali or Commercial Client"
    )
    testimonial = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonials'
    )
    featured = models.BooleanField(default=True)
    is_placeholder = models.BooleanField(
        default=False,
        help_text="Indicates editable placeholder awaiting real client review"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-featured', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.client_name} ({self.rating}★)"


class FAQ(models.Model):
    """
    Frequently Asked Questions.
    """
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(
        max_length=100,
        blank=True,
        default="General",
        help_text="e.g. General, Pricing, Process, Design"
    )
    display_order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Enquiry(models.Model):
    """
    Construction Quote & Project Enquiries.
    """
    STATUS_CHOICES = [
        ('new', 'New Enquiry'),
        ('contacted', 'Contacted'),
        ('quoted', 'Quoted'),
        ('in_progress', 'In Discussion / Progress'),
        ('completed', 'Completed / Won'),
        ('closed', 'Closed / Archived'),
    ]

    PROJECT_TYPE_CHOICES = [
        ('residential_new', 'New Residential Building / House'),
        ('commercial_new', 'Commercial Construction'),
        ('architectural_design', 'Architectural & Structural Design'),
        ('renovation_remodel', 'Renovation & Extension'),
        ('repairs_maintenance', 'Building Repairs & Maintenance'),
        ('landscaping', 'Landscaping & Exterior Works'),
        ('biodigester', 'Biodigester / Waste Management'),
        ('other', 'Other Building Solution'),
    ]

    BUDGET_CHOICES = [
        ('under_500k', 'Under KES 500,000'),
        ('500k_1m', 'KES 500,000 - 1,000,000'),
        ('1m_3m', 'KES 1,000,000 - 3,000,000'),
        ('3m_5m', 'KES 3,000,000 - 5,000,000'),
        ('5m_10m', 'KES 5,000,000 - 10,000,000'),
        ('above_10m', 'Above KES 10,000,000'),
        ('undecided', 'To Be Determined / Need Consultation'),
    ]

    START_DATE_CHOICES = [
        ('immediately', 'Immediately (Within 2 weeks)'),
        ('1_month', 'Within 1 Month'),
        ('1_3_months', '1 - 3 Months'),
        ('3_6_months', '3 - 6 Months'),
        ('planning', 'Currently in Planning Stage'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    phone = models.CharField(max_length=50, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email Address")
    location = models.CharField(max_length=150, blank=True, verbose_name="Project Location / County")
    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPE_CHOICES,
        default='residential_new',
        verbose_name="Project Category"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries',
        verbose_name="Specific Service (Optional)"
    )
    project_size = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Estimated Size (e.g. 4 Bedroom House, 500 sq m)"
    )
    preferred_start_date = models.CharField(
        max_length=50,
        choices=START_DATE_CHOICES,
        default='1_month',
        verbose_name="Preferred Start Timeline"
    )
    budget = models.CharField(
        max_length=50,
        choices=BUDGET_CHOICES,
        default='undecided',
        verbose_name="Budget Estimate"
    )
    description = models.TextField(verbose_name="Project Details & Scope")
    referral_source = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="How did you hear about us?"
    )
    attachment = models.FileField(
        upload_to=safe_attachment_path,
        blank=True,
        null=True,
        validators=[validate_file_extension],
        verbose_name="Project Document / Plan (PDF, JPG, PNG under 10MB)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    admin_notes = models.TextField(blank=True, help_text="Internal notes for company managers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project Enquiry / Quote Request"
        verbose_name_plural = "Project Enquiries & Quotes"

    def __str__(self):
        return f"Enquiry #{self.id} - {self.full_name} ({self.get_project_type_display()})"


class ContactMessage(models.Model):
    """
    General Contact Inquiries.
    """
    full_name = models.CharField(max_length=150, verbose_name="Full Name")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Phone Number")
    email = models.EmailField(verbose_name="Email Address")
    subject = models.CharField(max_length=200, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"
