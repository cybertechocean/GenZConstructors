#!/bin/bash
# ==============================================================================
# HostNali Shared Hosting Deployment & Update Script for Gen-Z Constructors
# Home Directory: /home2/genzcons
# Repository: https://github.com/cybertechocean/GenZConstructors
# ==============================================================================

set -e

echo "🚀 Starting Gen-Z Constructors deployment on HostNali..."

# 1. Ensure .env exists
if [ ! -f .env ]; then
    if [ -f .env.production ]; then
        echo "⚠️ .env not found. Copying from .env.production..."
        cp .env.production .env
        echo "📝 Please edit .env with your real MySQL and Secret Key values!"
    else
        echo "❌ .env file missing! Create .env before running deployment."
        exit 1
    fi
fi

# 2. Install / Update Dependencies
echo "📦 Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# 3. Run Database Migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# 4. Create Database Cache Table
echo "⚡ Creating / verifying cache table..."
python manage.py createcachetable

# 5. Seed Initial Data (if database is newly created)
echo "🌱 Checking and seeding initial data..."
python manage.py seed_data

# 6. Collect Static Assets with WhiteNoise compression
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 7. Restart Python App via touch on tmp/restart.txt or passenger_wsgi.py
mkdir -p tmp
touch tmp/restart.txt
touch passenger_wsgi.py

echo "✅ Deployment completed successfully! Website is live at https://genzconstructors.co.ke"
