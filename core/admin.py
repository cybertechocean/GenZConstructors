from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Service, Project, ProjectImage,
    ProcessStep, Testimonial, FAQ, Enquiry, ContactMessage
)

admin.site.site_header = "Gen-Z Constructors Administration"
admin.site.site_title = "Gen-Z Constructors Portal"
admin.site.index_title = "Website & Project Inquiries Management"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Company Identity", {
            'fields': ('business_name', 'tagline', 'website')
        }),
        ("Contact & Location", {
            'fields': ('phone', 'whatsapp_number', 'email', 'address', 'business_hours', 'map_embed_url')
        }),
        ("Social Profiles", {
            'fields': ('facebook_url', 'instagram_url', 'x_url', 'youtube_url')
        }),
        ("Brand Assets", {
            'fields': ('logo', 'favicon')
        }),
        ("Default SEO", {
            'fields': ('default_meta_title', 'default_meta_description')
        }),
    )

    def has_add_permission(self, request):
        # Only allow 1 instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon', 'featured', 'display_order', 'updated_at')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('featured', 'display_order')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2
    fields = ('image', 'caption', 'display_order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'status', 'featured', 'is_sample', 'display_order')
    list_filter = ('category', 'status', 'featured', 'is_sample')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('services',)
    list_editable = ('featured', 'display_order')
    inlines = [ProjectImageInline]


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'icon', 'display_order', 'active')
    list_editable = ('display_order', 'active')
    ordering = ('step_number',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'role_or_company', 'rating', 'featured', 'is_placeholder', 'created_at')
    list_filter = ('rating', 'featured', 'is_placeholder')
    search_fields = ('client_name', 'role_or_company', 'testimonial')
    list_editable = ('featured',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'display_order', 'active')
    list_filter = ('category', 'active')
    search_fields = ('question', 'answer')
    list_editable = ('display_order', 'active')


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'full_name', 'phone', 'email', 'project_type',
        'budget', 'status', 'created_at', 'has_attachment'
    )
    list_filter = ('status', 'project_type', 'preferred_start_date', 'budget', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'location', 'description')
    readonly_fields = ('created_at', 'updated_at', 'attachment_link')
    list_editable = ('status',)
    actions = ['mark_as_contacted', 'mark_as_quoted', 'mark_as_closed']

    fieldsets = (
        ("Client Details", {
            'fields': ('full_name', 'phone', 'email', 'location', 'referral_source')
        }),
        ("Project Details", {
            'fields': ('project_type', 'service', 'project_size', 'preferred_start_date', 'budget', 'description')
        }),
        ("Uploaded Documentation", {
            'fields': ('attachment', 'attachment_link')
        }),
        ("Status & Internal Notes", {
            'fields': ('status', 'admin_notes', 'created_at', 'updated_at')
        }),
    )

    def has_attachment(self, obj):
        return bool(obj.attachment)
    has_attachment.boolean = True
    has_attachment.short_description = "Attachment"

    def attachment_link(self, obj):
        if obj.attachment:
            return format_html('<a href="{}" target="_blank" class="button">Download Attachment</a>', obj.attachment.url)
        return "No attachment provided"
    attachment_link.short_description = "Download File"

    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
    mark_as_contacted.short_description = "Mark selected as Contacted"

    def mark_as_quoted(self, request, queryset):
        queryset.update(status='quoted')
    mark_as_quoted.short_description = "Mark selected as Quoted"

    def mark_as_closed(self, request, queryset):
        queryset.update(status='closed')
    mark_as_closed.short_description = "Mark selected as Closed"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'subject', 'message')
    list_editable = ('is_read',)
