# this file must be given in input to gunicorn, 
# and it is better that remains in root directory of the application.

import os
from django.core.wsgi import get_wsgi_application

# environment settings for Django app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainapp_ecommerce.settings')

# should be
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basic-django-ecommerce.settings')
# but in this case the main app descending from the project has been manually renamed.

# Initialize app Django
application = get_wsgi_application()
