# Gen-Z Constructors Limited Company

[![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Custom%20Design%20Tokens-38B2AC?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> **"Building Your Vision, Constructing Your Future."**

Official full-stack Django web application for **Gen-Z Constructors Limited Company**, a modern, client-focused construction and building solutions enterprise based in Nairobi, Kenya.

---

## 🌟 Key Features

- **Luxury Architectural Visual Identity**: Built with the official brand color system:
  - **Midnight Navy** (`#010B20`) & **Deep Dark** (`#08060A`)
  - **Rich Construction Gold** (`#B98F3D`) & **Light Champagne Gold** (`#EDDAA0`)
  - **Warm Ivory** (`#F1EDDF`) & **Architectural Light Canvas** (`#F8F7F3`)
  - Typography: **Space Grotesk** (Headings) & **Plus Jakarta Sans** (Body)
- **High-Conversion Customer Journey**:
  - **Hero Section**: Confident value proposition with instant quote, WhatsApp, and call CTAs.
  - **Services Catalog (`/services/` & `/services/<slug>/`)**: Detailed scopes, deliverable checklists, workflow phases, and tailored WhatsApp inquiry links.
  - **Portfolio Showcase (`/projects/` & `/projects/<slug>/`)**: Category-filtered project gallery with lightbox image modals and "Build Similar" inquiry CTAs.
  - **7-Step Construction Workflow (`/process/`)**: Transparent timeline from Consultation to Key Handover.
  - **Interactive Quotation System (`/request-a-quote/`)**: Multi-field lead capture with secure plan/document uploads (`.pdf`, `.jpg`, `.png`, `.webp` under 10MB) and instant WhatsApp quote continuation.
  - **Contact & Reach (`/contact/`)**: Direct phone, WhatsApp, email, Nairobi operating details, and inquiry form.
- **Mobile-First Conversions**:
  - Floating stacked **Phone Call** (`tel:+254713706103`) and **WhatsApp** chat buttons.
  - Fixed mobile bottom action bar (`[Call] [WhatsApp] [Quote]`) with safe-area spacing.
  - Smooth mobile slide-out navigation drawer.
- **Security & Anti-Spam**:
  - Built-in honeypot bot trap on forms.
  - Safe file upload validators with UUID filename hashing.
  - CSRF protection, secure headers, and production-ready `.env` configuration.
- **SEO & Social Optimization**:
  - Dynamic XML Sitemap (`/sitemap.xml`) & Robots policy (`/robots.txt`).
  - Open Graph & Twitter card previews.
  - JSON-LD Structured Data (`Organization`, `LocalBusiness`, `WebSite`).

---

## 🛠️ Technology Stack

- **Backend**: Python 3.11+, Django 6.1 (WSGI/ASGI compatible)
- **Database**: SQLite (local dev) / PostgreSQL or MySQL (production)
- **Frontend**: Django Templates, Vanilla CSS Design System, Tailwind CSS, Google Fonts, Lucide Icons, Font Awesome 6 Brands
- **Static Asset Delivery**: WhiteNoise
- **Deployment**: Compatible with cPanel Shared Hosting (Hostnali / Passenger WSGI), VPS (Nginx + Gunicorn), Render, Railway, DigitalOcean, Heroku

---

## 📁 Project Structure

```
GenZConstructors/
├── manage.py                   # Django CLI utility
├── passenger_wsgi.py           # Passenger WSGI entrypoint for cPanel/Shared hosting
├── requirements.txt            # Python dependencies
├── DEPLOYMENT.md               # Detailed Hostnali/cPanel deployment guide
├── .env.example                # Template for environment variables
├── .env                        # Local environment variables
│
├── config/                     # Django Project Configuration
│   ├── settings.py             # Global settings (WhiteNoise, context processors, DB)
│   ├── urls.py                 # Root URL configuration + Sitemaps + Error handlers
│   ├── wsgi.py                 # Standard WSGI configuration
│   └── asgi.py                 # ASGI configuration
│
├── core/                       # Main Application Module
│   ├── models.py               # Database models (SiteSettings, Service, Project, Enquiry, etc.)
│   ├── views.py                # View handlers & dynamic queries
│   ├── forms.py                # QuoteRequestForm & ContactForm with honeypot validation
│   ├── urls.py                 # Application URL routing
│   ├── admin.py                # Branded Django Admin with inline galleries & status filters
│   ├── context_processors.py   # Global site settings & dynamic WhatsApp helpers
│   ├── sitemaps.py             # Dynamic SEO sitemaps
│   ├── tests.py                # Comprehensive test suite (21 unit tests)
│   └── management/commands/    # Management CLI commands
│       └── seed_data.py        # Seed command for initial services, process, projects, FAQs
│
├── templates/                  # HTML5 Django Templates
│   ├── base.html               # Master layout with fonts, meta, and navigation
│   ├── 404.html, 403.html, 500.html # Branded error pages
│   ├── includes/               # Reusable partials (navbar, footer, whatsapp, mobile_cta, messages)
│   ├── home/index.html         # Homepage
│   ├── about/index.html        # About Us page
│   ├── services/               # Services listing & dynamic detail template
│   ├── projects/               # Projects portfolio & dynamic detail template
│   ├── process/index.html      # 7-Step Process page
│   ├── quote/                  # Request a Quote form & success confirmation
│   └── contact/index.html      # Contact Us page
│
├── static/                     # Static Assets
│   ├── css/style.css           # Master CSS design tokens & components
│   ├── js/main.js              # Interactivity, mobile menu drawer, lightbox modal
│   └── images/                 # Official logo, favicons (16x16, 32x32, 180x180), OG share images
│
└── media/                      # Uploaded Media
    ├── branding/               # Brand assets & logos
    ├── services/               # Service images
    ├── projects/               # Project portfolio photos & galleries
    └── enquiry_attachments/    # Secure user-uploaded blueprints and documents
```

---

## 🚀 Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/cybertechocean/GenZConstructors.git
cd GenZConstructors
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Seed Initial Data
Populate the database with services, 7-step process, sample projects, and Nairobi site settings:
```bash
python manage.py seed_data
```

### 7. Create Admin Superuser
```bash
python manage.py createsuperuser
```

### 8. Collect Static Files & Start Dev Server
```bash
python manage.py collectstatic --noinput
python manage.py runserver
```

Open your browser and visit:
- **Website**: `http://127.0.0.1:8000/`
- **Django Admin Portal**: `http://127.0.0.1:8000/admin/`

---

## 🧪 Running Tests

Run the automated Django test suite:
```bash
python manage.py test core
```
Run Django system health check:
```bash
python manage.py check
```

---

## 🌐 Production Deployment

For detailed deployment instructions on **Hostnali Web Hosting** (cPanel / CloudLinux Python App / Passenger WSGI), refer to:
👉 **[DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 📞 Business Information

- **Company**: Gen-Z Constructors Limited Company
- **Tagline**: *"Building Your Vision, Constructing Your Future."*
- **Location**: Nairobi, Kenya
- **Phone**: [+254 713 706 103](tel:+254713706103)
- **WhatsApp**: [+254 713 706 103](https://wa.me/254713706103)
- **Email**: [genzconstructors@gmail.com](mailto:genzconstructors@gmail.com)
- **Domain**: [genzconstructors.co.ke](https://genzconstructors.co.ke)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
