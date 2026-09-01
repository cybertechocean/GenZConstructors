# Deployment Guide: Gen-Z Constructors on Hostnali Shared Hosting

This guide provides a comprehensive, step-by-step walkthrough for deploying the **Gen-Z Constructors Limited Company** Django website from your GitHub repository onto **[Hostnali Web Hosting](https://hostnali.co.ke)** (cPanel with CloudLinux *Setup Python App* / Passenger WSGI).

---

## 1. Prerequisites

Before starting, ensure you have:
1. An active **Hostnali cPanel hosting account** (e.g. Bronze, Silver, or Gold plan with Python App support).
2. Your registered domain name (e.g. `genzconstructors.co.ke` or a subdomain `demo.genzconstructors.co.ke`) pointed to Hostnali nameservers.
3. Access to your **GitHub repository** containing this codebase.
4. Access to **cPanel** dashboard provided by Hostnali.

---

## 2. Step-by-Step Deployment Workflow

```
[GitHub Repository]
       │
       ▼ (Git Clone / Version Control in cPanel)
[Hostnali Server: /home/username/GenZConstructors]
       │
       ▼ (Setup Python App in cPanel)
[Virtualenv Creation & Dependencies: requirements.txt]
       │
       ▼ (Database & Static Files)
[python manage.py migrate && python manage.py seed_data && collectstatic]
       │
       ▼ (Passenger WSGI + SSL)
[LIVE: https://genzconstructors.co.ke]
```

---

### Step 1: Clone Your GitHub Repository to Hostnali

You can clone your repository using either **cPanel Git Version Control** or the **cPanel Terminal**.

#### Option A: Using cPanel Git™ Version Control (Recommended)
1. Log in to your **Hostnali cPanel**.
2. Under the **Files** section, click on **Git™ Version Control**.
3. Click the **Create** button (top right).
4. Fill in the repository details:
   - **Clone URL**: `https://github.com/your-username/GenZConstructors.git`
   - **Repository Path**: `GenZConstructors` (or `public_html` / your preferred folder)
   - **Repository Name**: `GenZConstructors`
5. Click **Create**. cPanel will clone your repository from GitHub.

#### Option B: Using cPanel Terminal (SSH)
1. In cPanel, open **Terminal** (under *Advanced*).
2. Run:
   ```bash
   cd ~
   git clone https://github.com/your-username/GenZConstructors.git
   ```

---

### Step 2: Create the Python Application in cPanel

1. In cPanel, navigate to the **Software** section and click on **Setup Python App**.
2. Click **Create Application**.
3. Configure the application settings:
   - **Python version**: Select **3.11.x** or **3.12.x** (recommended).
   - **Application root**: `GenZConstructors` (the folder where your repo is cloned).
   - **Application URL**: Select your domain (e.g. `genzconstructors.co.ke` or leave blank for root).
   - **Application startup file**: `passenger_wsgi.py` (included in the root of this repo).
   - **Application Entry point**: `application`
4. Click **Create** at the top right.
5. Once created, cPanel will display a command at the top to activate the virtual environment, for example:
   ```bash
   source /home/username/virtualenv/GenZConstructors/3.11/bin/activate && cd /home/username/GenZConstructors
   ```
   *Copy this command.*

---

### Step 3: Configure Environment Variables (`.env`)

1. In cPanel, open **File Manager** and navigate to your application root (`/home/username/GenZConstructors/`).
2. If `.env` is not visible, click **Settings** (top right in File Manager) and check **Show Hidden Files (dotfiles)**.
3. Create or edit `.env` in the project root:
   ```env
   DEBUG=False
   SECRET_KEY=your-secure-random-secret-key-change-this-in-production
   ALLOWED_HOSTS=genzconstructors.co.ke,www.genzconstructors.co.ke,localhost,127.0.0.1
   
   # Static and Media
   COMPANY_PHONE=+254713706103
   COMPANY_WHATSAPP=254713706103
   COMPANY_EMAIL=genzconstructors@gmail.com
   COMPANY_DOMAIN=genzconstructors.co.ke
   
   # Optional: Email SMTP Configuration for lead alerts
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=genzconstructors@gmail.com
   EMAIL_HOST_PASSWORD=your-gmail-app-password
   DEFAULT_FROM_EMAIL=Gen-Z Constructors <genzconstructors@gmail.com>
   ```

---

### Step 4: Install Dependencies & Run Database Migrations

1. In cPanel, open **Terminal**.
2. Paste the virtualenv activation command you copied in Step 2:
   ```bash
   source /home/username/virtualenv/GenZConstructors/3.11/bin/activate && cd /home/username/GenZConstructors
   ```
3. Install all required dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Seed initial data (Services, 7-Step Process, Nairobi settings, FAQs):
   ```bash
   python manage.py seed_data
   ```
6. Create an administrator superuser to manage the portal:
   ```bash
   python manage.py createsuperuser
   ```
   *(Enter your desired admin username, email, and password)*

---

### Step 5: Collect Static Files & Configure `.htaccess`

1. In the same terminal session with virtualenv active, run:
   ```bash
   python manage.py collectstatic --noinput
   ```
2. Check your `.htaccess` file in `public_html` or application root to ensure static and media requests are served cleanly by Apache/LiteSpeed:
   ```apache
   # DO NOT REMOVE PASSENGER SETTINGS
   PassengerAppRoot "/home/username/GenZConstructors"
   PassengerPython "/home/username/virtualenv/GenZConstructors/3.11/bin/python"

   # Serve static files directly
   RewriteEngine On
   RewriteRule ^static/(.*)$ /home/username/GenZConstructors/staticfiles/$1 [L]
   RewriteRule ^media/(.*)$ /home/username/GenZConstructors/media/$1 [L]
   ```

---

### Step 6: Enable Free SSL Certificate (HTTPS)

1. In cPanel, go to **Security** $\to$ **SSL/TLS Status**.
2. Select your domain (`genzconstructors.co.ke` and `www.genzconstructors.co.ke`).
3. Click **Run AutoSSL**. Hostnali will issue a free Let's Encrypt SSL certificate within a few minutes.
4. In cPanel, go to **Domains** and toggle **Force HTTPS Redirect** to **ON**.

---

### Step 7: Restart the Python App

1. In cPanel, go back to **Setup Python App**.
2. Next to your application, click the **Restart** button (circular arrow icon).
3. Visit `https://genzconstructors.co.ke` in your browser!

---

## 3. How to Update the Website in Future from GitHub

Whenever you push new updates to your GitHub repository:

1. Open **cPanel Terminal** (or use **Git Version Control** in cPanel $\to$ **Pull**).
2. Activate your virtualenv:
   ```bash
   source /home/username/virtualenv/GenZConstructors/3.11/bin/activate && cd /home/username/GenZConstructors
   ```
3. Pull the latest commits:
   ```bash
   git pull origin main
   ```
4. Run migrations and collect static files if changes were made:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
5. Restart the Python App:
   - In cPanel $\to$ **Setup Python App** $\to$ Click **Restart**.
   - Or in terminal: `touch tmp/restart.txt`

---

## 4. Troubleshooting Common Shared Hosting Issues

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **500 Internal Server Error** | Missing `.env`, syntax error in `passenger_wsgi.py`, or missing package | Check cPanel error log or stderr log in `GenZConstructors/` folder. Ensure all packages from `requirements.txt` are installed. |
| **Static files (CSS/Images) not loading** | `collectstatic` was not run or path mismatch in `.htaccess` | Run `python manage.py collectstatic --noinput` inside the activated virtualenv and verify `STATIC_ROOT`. |
| **Changes not showing after git pull** | Passenger caching running process | Click **Restart** in cPanel **Setup Python App** or run `touch tmp/restart.txt`. |
| **DisallowedHost Error** | Domain not listed in `ALLOWED_HOSTS` | Add your exact domain (e.g. `genzconstructors.co.ke,www.genzconstructors.co.ke`) to `ALLOWED_HOSTS` in `.env`. |
