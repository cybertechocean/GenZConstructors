import re
from django import forms
from .models import Enquiry, ContactMessage, Service

class HoneypotForm(forms.ModelForm):
    """
    Base form including an invisible honeypot field to trap automated bots.
    """
    website_url_hp = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none !important;',
            'tabindex': '-1',
            'autocomplete': 'off',
            'aria-hidden': 'true'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        hp = cleaned_data.get('website_url_hp')
        if hp:
            # Trap bot submission silently or raise
            raise forms.ValidationError("Invalid form submission detected.")
        return cleaned_data


class QuoteRequestForm(HoneypotForm):
    """
    Detailed quote request form for construction enquiries.
    """
    class Meta:
        model = Enquiry
        fields = [
            'full_name',
            'phone',
            'email',
            'location',
            'project_type',
            'service',
            'project_size',
            'preferred_start_date',
            'budget',
            'description',
            'referral_source',
            'attachment',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Alex Mwangi',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. +254 712 345 678',
                'required': True,
                'type': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. alex@example.com',
                'required': True,
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Westlands, Nairobi / Karen / Kiambu',
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'service': forms.Select(attrs={
                'class': 'form-select',
            }),
            'project_size': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. 4 Bedroom Maisonette / 450 sqm',
            }),
            'preferred_start_date': forms.Select(attrs={
                'class': 'form-select',
            }),
            'budget': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Describe your project, requirements, site conditions, or special considerations...',
                'required': True,
            }),
            'referral_source': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Google, Instagram, Facebook, Referral',
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-file',
                'accept': '.pdf,.jpg,.jpeg,.png,.webp',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.all().order_by('display_order', 'name')
        self.fields['service'].empty_label = "-- Select Specific Service (Optional) --"

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        # Basic check for reasonable phone numbers
        clean_num = re.sub(r'[\s\-\(\)\+]', '', phone)
        if len(clean_num) < 9 or len(clean_num) > 15:
            raise forms.ValidationError("Please provide a valid phone number with area code (e.g. +254 712 345 678).")
        return phone


class ContactForm(HoneypotForm):
    """
    Standard contact & general enquiry form.
    """
    class Meta:
        model = ContactMessage
        fields = [
            'full_name',
            'phone',
            'email',
            'subject',
            'message',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Full Name',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Phone Number (e.g. +254 712 345 678)',
                'type': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Email Address',
                'required': True,
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Subject / Topic',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'How can we help you?',
                'required': True,
            }),
        }
