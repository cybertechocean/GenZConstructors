import os
import sys

# Add project root directory to python path
project_home = os.path.dirname(os.path.abspath(__file__))
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
