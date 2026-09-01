from django.core.management.base import BaseCommand
from core.models import (
    SiteSettings, Service, Project, ProcessStep,
    Testimonial, FAQ
)

class Command(BaseCommand):
    help = 'Seeds initial database records for Gen-Z Constructors Limited Company'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Gen-Z Constructors initial data..."))

        # 1. Site Settings
        settings_obj = SiteSettings.load()
        settings_obj.business_name = "Gen-Z Constructors Limited Company"
        settings_obj.tagline = "BUILDING YOUR VISION, CONSTRUCTING YOUR FUTURE."
        settings_obj.phone = "+254713706103"
        settings_obj.whatsapp_number = "254713706103"
        settings_obj.email = "genzconstructors@gmail.com"
        settings_obj.website = "genzconstructors.co.ke"
        settings_obj.address = "Nairobi, Kenya"
        settings_obj.business_hours = "Mon - Fri: 8:00 AM - 5:00 PM | Sat: 8:00 AM - 1:00 PM"
        settings_obj.facebook_url = "https://facebook.com/genzconstructors"
        settings_obj.instagram_url = "https://instagram.com/genzconstructors"
        settings_obj.logo = "branding/logo.jpg"
        settings_obj.favicon = "branding/logo.jpg"
        settings_obj.default_meta_title = "Gen-Z Constructors Limited Company | Construction & Building Solutions"
        settings_obj.default_meta_description = "Gen-Z Constructors Limited Company delivers modern construction, architectural design, structural engineering, renovations and building solutions across Kenya. Building Your Vision, Constructing Your Future."
        settings_obj.save()
        self.stdout.write(self.style.SUCCESS("[OK] Site settings configured"))

        # 2. Services
        services_data = [
            {
                'name': 'Building Construction',
                'slug': 'building-construction',
                'category': 'construction',
                'icon': 'building-2',
                'short_description': 'Full-cycle residential and commercial construction executed with premium structural integrity.',
                'description': 'From foundation laying to final roof installation and interior finishes, Gen-Z Constructors handles all phases of building construction. We combine modern engineering practices with strict quality control to deliver spaces built to last.',
                'key_features': 'Complete turnkey building construction\nReinforced concrete and masonry works\nStrict structural standards & quality supervision\nTransparent progress updates and milestone management',
                'featured': True,
                'display_order': 1,
            },
            {
                'name': 'Architectural Design',
                'slug': 'architectural-design',
                'category': 'design',
                'icon': 'pen-tool',
                'short_description': 'Contemporary architectural blueprints, 3D visualizations, and functional modern layouts.',
                'description': 'Our architectural design approach marries aesthetic elegance with space optimization and climatic comfort. We produce fully compliant CAD drawings, realistic 3D renderings, and county-ready documentation.',
                'key_features': 'Custom architectural blueprints & concept drawings\n3D photorealistic visualization & walkthroughs\nSpace planning & passive climate adaptation\nCounty approval submission support',
                'featured': True,
                'display_order': 2,
            },
            {
                'name': 'Structural Solutions',
                'slug': 'structural-solutions',
                'category': 'design',
                'icon': 'hard-hat',
                'short_description': 'Precision structural engineering calculations, reinforcement details, and load analysis.',
                'description': 'We provide comprehensive structural engineering assessments, foundation designs, and structural reinforcement plans to ensure safety, durability, and compliance with Kenyan building codes.',
                'key_features': 'Structural integrity assessments\nFoundation engineering & soil load calculations\nSteel and reinforced concrete design details\nSite structural supervision',
                'featured': True,
                'display_order': 3,
            },
            {
                'name': 'Project Planning & Management',
                'slug': 'project-planning',
                'category': 'construction',
                'icon': 'compass',
                'short_description': 'Detailed costing, Bills of Quantities (BOQ), site supervision, and milestone tracking.',
                'description': 'Smooth construction execution starts with rigorous planning. We provide accurate BOQs, cost estimates, material procurement management, and on-site oversight to avoid delays and cost overruns.',
                'key_features': 'Accurate Bill of Quantities (BOQ) preparation\nProject timeline and Gantt chart scheduling\nMaterial procurement & supply chain oversight\nOn-site quality supervision',
                'featured': True,
                'display_order': 4,
            },
            {
                'name': 'Building Renovation & Remodeling',
                'slug': 'building-renovation',
                'category': 'renovation',
                'icon': 'hammer',
                'short_description': 'Transforming existing residential and commercial properties with modern finishes.',
                'description': 'Breathe new life into aging structures with our remodeling and expansion services. We handle structural modifications, modern tile and ceiling works, plumbing and electrical upgrades.',
                'key_features': 'Interior & exterior remodeling\nStructural additions and floor plan reconfiguration\nTile, ceiling, and modern painting finishes\nElectrical and plumbing modernizations',
                'featured': True,
                'display_order': 5,
            },
            {
                'name': 'Repairs & Maintenance',
                'slug': 'repairs-maintenance',
                'category': 'renovation',
                'icon': 'wrench',
                'short_description': 'Reliable structural repairs, waterproofing, cracking fixes, and building maintenance.',
                'description': 'Protect your property investment with timely repairs. We diagnose water seepage, foundation settling, masonry cracks, and roof leakages, providing durable remediation.',
                'key_features': 'Waterproofing and damp-proofing solutions\nMasonry crack repair and structural strengthening\nRoofing leak diagnosis and repairs\nRoutine facility maintenance contracts',
                'featured': False,
                'display_order': 6,
            },
            {
                'name': 'Landscaping & Exterior Solutions',
                'slug': 'landscaping',
                'category': 'specialized',
                'icon': 'trees',
                'short_description': 'Cabro paving, perimeter walling, drainage channels, and functional outdoor spaces.',
                'description': 'Elevate your property curb appeal with our exterior and compound solutions. We install durable cabro paving, boundary walls, security gates, and modern drainage systems.',
                'key_features': 'Heavy-duty and decorative cabro paving\nPerimeter boundary walling and security fencing\nCompound storm water drainage engineering\nOutdoor functional living spaces',
                'featured': False,
                'display_order': 7,
            },
            {
                'name': 'Biodigester Solutions',
                'slug': 'biodigester-solutions',
                'category': 'specialized',
                'icon': 'droplet',
                'short_description': 'Modern eco-friendly wastewater biodigester systems for residential and commercial sites.',
                'description': 'Replace obsolete septic tanks with modern, smell-free, self-recycling biological waste digesters. Engineered for long-term reliability and minimal maintenance.',
                'key_features': 'Modern biological waste treatment tanks\nEco-friendly & odour-free operation\nCost-effective alternative to traditional septic pits\nCompact footprint and long lifespan',
                'featured': False,
                'display_order': 8,
            },
        ]

        created_services = {}
        for s_data in services_data:
            slug = s_data.pop('slug')
            obj, created = Service.objects.update_or_create(slug=slug, defaults=s_data)
            created_services[slug] = obj
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(created_services)} services configured"))

        # 3. Process Steps (7 Steps)
        process_data = [
            {
                'step_number': 1,
                'title': 'Consultation & Discovery',
                'subtitle': 'Understanding your vision',
                'description': 'We sit down with you to understand your project requirements, aesthetic preferences, budget boundaries, and timeline expectations.',
                'icon': 'message-square',
                'display_order': 1,
            },
            {
                'step_number': 2,
                'title': 'Project Assessment',
                'subtitle': 'Evaluating the site & terrain',
                'description': 'Our technical team conducts site visits, assesses soil conditions, checks zoning regulations, and determines logistical requirements.',
                'icon': 'map-pin',
                'display_order': 2,
            },
            {
                'step_number': 3,
                'title': 'Planning & Design',
                'subtitle': 'Blueprint & engineering plans',
                'description': 'We craft detailed architectural plans, structural engineering calculations, 3D visualizations, and assist with municipal approval documentation.',
                'icon': 'pen-tool',
                'display_order': 3,
            },
            {
                'step_number': 4,
                'title': 'Costing & Quotation',
                'subtitle': 'Transparent Bill of Quantities',
                'description': 'We provide a clear, itemized Bill of Quantities (BOQ) with realistic milestone pricing so you have complete visibility without hidden costs.',
                'icon': 'calculator',
                'display_order': 4,
            },
            {
                'step_number': 5,
                'title': 'Preparation & Mobilization',
                'subtitle': 'Groundwork and procurement',
                'description': 'We procure verified quality building materials, mobilize qualified artisans, and set up site safety protocols prior to breaking ground.',
                'icon': 'truck',
                'display_order': 5,
            },
            {
                'step_number': 6,
                'title': 'Construction Execution',
                'subtitle': 'Precision structural building',
                'description': 'Construction proceeds following strict engineering tolerances, scheduled milestone reviews, and regular photo/video updates to the client.',
                'icon': 'hammer',
                'display_order': 6,
            },
            {
                'step_number': 7,
                'title': 'Inspection & Handover',
                'subtitle': 'Quality check and key handover',
                'description': 'A comprehensive final walkthrough and finishing audit is conducted. Once satisfied with every detail, we officially hand over your completed space.',
                'icon': 'check-circle-2',
                'display_order': 7,
            },
        ]

        for p_data in process_data:
            step_num = p_data.pop('step_number')
            ProcessStep.objects.update_or_create(step_number=step_num, defaults=p_data)
        self.stdout.write(self.style.SUCCESS("[OK] 7-step construction process configured"))

        # 4. Sample Projects (Clearly flagged as sample projects for easy replacement)
        projects_data = [
            {
                'title': 'Modern Executive Villa Residence',
                'slug': 'modern-executive-villa-residence',
                'category': 'residential',
                'location': 'Nairobi, Kenya',
                'status': 'completed',
                'short_description': 'Contemporary 4-bedroom multi-level residence with flat roof aesthetics and open-concept living.',
                'description': 'A sample residential building project demonstrating modern architecture, large glass apertures for natural lighting, and robust reinforced concrete construction designed for structural longevity.',
                'scope_of_work': 'Architectural design & 3D renderings\nFoundation & structural concrete framing\nCustom modern interior finishes & tiling\nExterior landscaping & cabro compound paving',
                'featured': True,
                'is_sample': True,
                'display_order': 1,
                'services': ['building-construction', 'architectural-design', 'structural-solutions'],
            },
            {
                'title': 'Commercial Office & Retail Hub',
                'slug': 'commercial-office-retail-hub',
                'category': 'commercial',
                'location': 'Nairobi Commercial District',
                'status': 'completed',
                'short_description': 'Multi-storey commercial development engineered for flexible office spaces and modern retail storefronts.',
                'description': 'Sample commercial building showcase emphasizing high-efficiency structural column grids, modern curtain-wall facades, and heavy-duty utility integration.',
                'scope_of_work': 'Structural calculations & reinforced column layout\nCommercial grade partition walls & glass facades\nStormwater management & biodigester installation\nPerimeter boundary security walling',
                'featured': True,
                'is_sample': True,
                'display_order': 2,
                'services': ['building-construction', 'structural-solutions', 'biodigester-solutions'],
            },
            {
                'title': 'Executive Residential Remodel & Extension',
                'slug': 'executive-residential-remodel-extension',
                'category': 'renovation',
                'location': 'Nairobi Suburbs',
                'status': 'completed',
                'short_description': 'Full interior and structural remodeling of an existing property into a modern luxury dwelling.',
                'description': 'Sample renovation project demonstrating room reconfiguration, modern gypsum ceilings, high-end tiling, and exterior damp-proofing restoration.',
                'scope_of_work': 'Structural wall removal and steel beam support\nGypsum ceilings with integrated ambient lighting\nComplete kitchen and bathroom plumbing overhaul\nWaterproofing and exterior textured painting',
                'featured': True,
                'is_sample': True,
                'display_order': 3,
                'services': ['building-renovation', 'repairs-maintenance'],
            },
            {
                'title': 'Eco-Friendly Compound & Landscape Works',
                'slug': 'eco-friendly-compound-landscape-works',
                'category': 'landscaping',
                'location': 'Nairobi Environs',
                'status': 'completed',
                'short_description': 'Complete exterior paved grounds, biological waste treatment, and aesthetic boundary solutions.',
                'description': 'Sample exterior works project showcasing interlocking paving blocks, sustainable biodigester installation, and integrated garden drainage.',
                'scope_of_work': 'Heavy-duty cabro block installation\nEco-digester biological septic installation\nPerimeter masonry walling & automated gate track\nStorm drain grading and collection sumps',
                'featured': False,
                'is_sample': True,
                'display_order': 4,
                'services': ['landscaping', 'biodigester-solutions'],
            },
        ]

        for proj in projects_data:
            slug = proj.pop('slug')
            services_keys = proj.pop('services', [])
            p_obj, created = Project.objects.update_or_create(slug=slug, defaults=proj)
            for s_key in services_keys:
                if s_key in created_services:
                    p_obj.services.add(created_services[s_key])
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(projects_data)} sample projects configured"))

        # 5. Placeholder Testimonials (Clearly labeled)
        testimonials_data = [
            {
                'client_name': 'Sample Client - Residential Project',
                'role_or_company': 'Homeowner, Nairobi',
                'testimonial': 'Gen-Z Constructors approached our project with exceptional professionalism and attention to structural details. Their communication and milestone delivery was clear throughout.',
                'rating': 5,
                'featured': True,
                'is_placeholder': True,
            },
            {
                'client_name': 'Sample Client - Commercial Renovation',
                'role_or_company': 'Property Manager, Nairobi',
                'testimonial': 'The team delivered our renovation on schedule and maintained clean, organized site standards. Highly recommended for modern building solutions.',
                'rating': 5,
                'featured': True,
                'is_placeholder': True,
            },
        ]

        for t_data in testimonials_data:
            Testimonial.objects.update_or_create(
                client_name=t_data['client_name'],
                defaults=t_data
            )
        self.stdout.write(self.style.SUCCESS("[OK] Testimonials placeholder data configured"))

        # 6. FAQs
        faqs_data = [
            {
                'question': 'What construction and building services do you offer?',
                'answer': 'Gen-Z Constructors Limited Company provides full-cycle building construction, architectural design & 3D rendering, structural engineering solutions, project planning & BOQs, building renovations, structural repairs, landscaping/paving, and biological waste digester systems.',
                'category': 'Services',
                'display_order': 1,
            },
            {
                'question': 'How do I request a project quotation?',
                'answer': 'You can request a quotation by filling out our online "Request a Quote" form, calling us at +254 713 706 103, or messaging us directly on WhatsApp. We will review your project scope and arrange a consultation.',
                'category': 'Quotation',
                'display_order': 2,
            },
            {
                'question': 'What is your construction workflow?',
                'answer': 'We follow a structured 7-step process: Consultation -> Project Assessment -> Planning & Design -> Costing & BOQ -> Preparation & Mobilization -> Construction Execution -> Inspection & Handover.',
                'category': 'Process',
                'display_order': 3,
            },
            {
                'question': 'Do you handle architectural drawings and municipal approvals?',
                'answer': 'Yes, our architectural and design team prepares compliant architectural blueprints, structural engineering calculations, and 3D models ready for local authority review and approval.',
                'category': 'Design',
                'display_order': 4,
            },
            {
                'question': 'Can you work on existing buildings for renovation or repairs?',
                'answer': 'Yes, we provide extensive remodeling, structural reinforcement, waterproofing, and modernization for existing commercial and residential buildings.',
                'category': 'Renovation',
                'display_order': 5,
            },
            {
                'question': 'Where does Gen-Z Constructors operate?',
                'answer': 'We are based in Nairobi, Kenya, handling projects across Nairobi, surrounding counties, and nationwide.',
                'category': 'General',
                'display_order': 6,
            },
        ]

        for f_data in faqs_data:
            FAQ.objects.update_or_create(
                question=f_data['question'],
                defaults=f_data
            )
        self.stdout.write(self.style.SUCCESS("[OK] FAQs configured"))

        self.stdout.write(self.style.SUCCESS("[DONE] Seeding complete! Database is populated with production-ready structure."))
