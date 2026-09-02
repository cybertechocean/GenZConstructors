"""
Passenger WSGI Configuration for HostNali / cPanel Python Application.
Home Directory: /home2/genzcons
Repository: https://github.com/cybertechocean/GenZConstructors
"""

import sys
import os

# Add application directory to python path
APPLICATION_DIR = os.path.dirname(os.path.abspath(__file__))
if APPLICATION_DIR not in sys.path:
    sys.path.insert(0, APPLICATION_DIR)

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
