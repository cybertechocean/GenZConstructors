from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import (
    SiteSettings, Service, Project, ProcessStep,
    Testimonial, FAQ, Enquiry, ContactMessage
)
from .forms import QuoteRequestForm, ContactForm


class ModelTests(TestCase):
    def setUp(self):
        self.settings = SiteSettings.load()
        self.service = Service.objects.create(
            name="Turnkey Construction",
            category="construction",
            short_description="Full building services",
            description="Detailed turnkey construction description",
            key_features="Foundation\nFraming\nFinishing",
            icon="building-2"
        )
        self.project = Project.objects.create(
            title="Modern Executive Villa Project",
            category="residential",
            location="Nairobi",
            status="completed",
            short_description="Luxury 4 bedroom home",
            description="Detailed construction overview",
            scope_of_work="Foundation\nRoofing\nInteriors",
        )
        self.project.services.add(self.service)

    def test_site_settings_singleton(self):
        self.assertEqual(self.settings.business_name, "Gen-Z Constructors Limited Company")
        # Ensure second load returns same instance
        settings2 = SiteSettings.load()
        self.assertEqual(self.settings.pk, settings2.pk)

    def test_service_model(self):
        self.assertEqual(self.service.slug, "turnkey-construction")
        self.assertEqual(self.service.get_absolute_url(), "/services/turnkey-construction/")
        features = self.service.get_features_list()
        self.assertEqual(len(features), 3)
        self.assertIn("Foundation", features)

    def test_project_model(self):
        self.assertEqual(self.project.slug, "modern-executive-villa-project")
        self.assertEqual(self.project.get_absolute_url(), "/projects/modern-executive-villa-project/")
        scope = self.project.get_scope_list()
        self.assertEqual(len(scope), 3)

    def test_process_step_model(self):
        step = ProcessStep.objects.create(
            step_number=1,
            title="Consultation",
            description="Initial discussion"
        )
        self.assertEqual(str(step), "01. Consultation")

    def test_faq_model(self):
        faq = FAQ.objects.create(
            question="What is your timeline?",
            answer="Timelines depend on project size."
        )
        self.assertEqual(str(faq), "What is your timeline?")

    def test_testimonial_model(self):
        t = Testimonial.objects.create(
            client_name="Jane Doe",
            role_or_company="Homeowner",
            testimonial="Excellent quality workmanship.",
            rating=5
        )
        self.assertIn("Jane Doe", str(t))


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.settings = SiteSettings.load()
        self.service = Service.objects.create(
            name="Architectural Design",
            category="design",
            short_description="Plans & 3D models",
            description="Complete blueprint services",
            icon="pen-tool"
        )
        self.project = Project.objects.create(
            title="Urban Plaza",
            category="commercial",
            location="Nairobi",
            status="completed",
            short_description="Commercial building",
            description="Commercial building details",
        )

    def test_home_view(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gen-Z Constructors")
        self.assertTemplateUsed(response, 'home/index.html')

    def test_about_view(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/index.html')

    def test_services_list_view(self):
        response = self.client.get(reverse('core:services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Architectural Design")

    def test_service_detail_view(self):
        response = self.client.get(reverse('core:service_detail', kwargs={'slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Architectural Design")
        self.assertContains(response, "WhatsApp Inquiry")

    def test_service_detail_404(self):
        response = self.client.get(reverse('core:service_detail', kwargs={'slug': 'non-existent-service'}))
        self.assertEqual(response.status_code, 404)

    def test_projects_list_view(self):
        response = self.client.get(reverse('core:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Urban Plaza")

    def test_project_detail_view(self):
        response = self.client.get(reverse('core:project_detail', kwargs={'slug': self.project.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Urban Plaza")

    def test_process_view(self):
        response = self.client.get(reverse('core:process'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'process/index.html')

    def test_contact_get(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/index.html')

    def test_request_quote_get(self):
        response = self.client.get(reverse('core:request_quote'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quote/index.html')

    def test_robots_txt(self):
        response = self.client.get(reverse('core:robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/plain')
        self.assertIn(b"User-agent", response.content)

    def test_sitemap_xml(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"urlset", response.content)


class FormAndWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = Service.objects.create(
            name="Building Construction",
            category="construction",
            short_description="Full construction",
            description="Details"
        )

    def test_quote_request_submission_success(self):
        data = {
            'full_name': 'John Mwangi',
            'phone': '+254712345678',
            'email': 'john@example.com',
            'location': 'Nairobi',
            'project_type': 'residential_new',
            'service': self.service.id,
            'project_size': '4 Bedroom Maisonette',
            'preferred_start_date': '1_month',
            'budget': '3m_5m',
            'description': 'We want to construct a four-bedroom house on a 50x100 plot.',
            'referral_source': 'Google Search',
            'website_url_hp': '',  # Honeypot empty
        }
        response = self.client.post(reverse('core:request_quote'), data)
        self.assertEqual(response.status_code, 302)
        
        # Verify Enquiry record was created
        enquiry = Enquiry.objects.get(email='john@example.com')
        self.assertEqual(enquiry.full_name, 'John Mwangi')
        self.assertEqual(enquiry.service, self.service)
        self.assertEqual(enquiry.status, 'new')

        # Follow to success page
        success_url = reverse('core:quote_success', kwargs={'pk': enquiry.id})
        success_response = self.client.get(success_url)
        self.assertEqual(success_response.status_code, 200)
        self.assertContains(success_response, "Thank You, John Mwangi!")
        self.assertContains(success_response, f"Enquiry Reference #{enquiry.id}")

    def test_quote_request_honeypot_trap(self):
        data = {
            'full_name': 'Bot Spammer',
            'phone': '+254700000000',
            'email': 'bot@spam.com',
            'project_type': 'residential_new',
            'description': 'Spam message',
            'website_url_hp': 'http://spam-link.com',  # Filled honeypot
        }
        response = self.client.post(reverse('core:request_quote'), data)
        self.assertEqual(response.status_code, 200)
        # Should not create Enquiry
        self.assertFalse(Enquiry.objects.filter(email='bot@spam.com').exists())

    def test_contact_form_submission(self):
        data = {
            'full_name': 'Grace Achieng',
            'phone': '+254722112233',
            'email': 'grace@example.com',
            'subject': 'General Inquiry about Design',
            'message': 'Hello, do you offer consultations on modern climate-responsive designs?',
            'website_url_hp': '',
        }
        response = self.client.post(reverse('core:contact'), data)
        self.assertEqual(response.status_code, 302)
        
        contact_msg = ContactMessage.objects.get(email='grace@example.com')
        self.assertEqual(contact_msg.full_name, 'Grace Achieng')
        self.assertEqual(contact_msg.subject, 'General Inquiry about Design')

    def test_testimonials_view(self):
        Testimonial.objects.create(
            client_name="Sarah Mutua",
            role_or_company="Homeowner, Karen",
            testimonial="The Gen-Z team handled our house with utmost professionalism.",
            rating=5,
            featured=True
        )
        response = self.client.get(reverse('core:testimonials'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "What Our Clients Say")
        self.assertContains(response, "Sarah Mutua")
        self.assertContains(response, "The Gen-Z team handled our house")

    def test_faqs_view(self):
        FAQ.objects.create(
            question="Do you help with county building approval?",
            answer="Yes, our architectural team submits and secures county building approvals.",
            category="Permits",
            active=True
        )
        response = self.client.get(reverse('core:faqs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frequently Asked Questions")
        self.assertContains(response, "Do you help with county building approval?")

    def test_image_url_support_and_service_gallery(self):
        from .models import ServiceImage, ProjectImage
        # Test Service featured_image_url
        service_with_url = Service.objects.create(
            name="Roofing Solutions",
            category="specialized",
            short_description="Roofing works",
            description="Detailed roofing works",
            featured_image_url="https://images.unsplash.com/photo-roofing.jpg"
        )
        self.assertEqual(service_with_url.get_featured_image_url, "https://images.unsplash.com/photo-roofing.jpg")

        # Test ServiceImage with image_url
        svc_img = ServiceImage.objects.create(
            service=service_with_url,
            image_url="https://images.unsplash.com/photo-gallery-1.jpg",
            caption="Roof Truss Installation"
        )
        self.assertEqual(svc_img.get_image_url, "https://images.unsplash.com/photo-gallery-1.jpg")

        # Test Project featured_image_url
        project_with_url = Project.objects.create(
            title="Commercial Warehousing",
            category="commercial",
            short_description="Heavy duty warehouse",
            description="Warehouse description",
            featured_image_url="https://images.unsplash.com/photo-warehouse.jpg"
        )
        self.assertEqual(project_with_url.get_featured_image_url, "https://images.unsplash.com/photo-warehouse.jpg")

        # Test ProjectImage with image_url
        proj_img = ProjectImage.objects.create(
            project=project_with_url,
            image_url="https://images.unsplash.com/photo-proj-gallery.jpg",
            caption="Steel Erection"
        )
        self.assertEqual(proj_img.get_image_url, "https://images.unsplash.com/photo-proj-gallery.jpg")

    def test_admin_changelist_no_typeerror(self):
        from django.contrib.auth.models import User
        superuser = User.objects.create_superuser('admin_tester', 'admin@test.com', 'password123')
        self.client.login(username='admin_tester', password='password123')

        # Check project changelist (where format_html TypeError occurred previously)
        proj_resp = self.client.get('/admin/core/project/')
        self.assertEqual(proj_resp.status_code, 200)

        # Check service changelist
        svc_resp = self.client.get('/admin/core/service/')
        self.assertEqual(svc_resp.status_code, 200)
