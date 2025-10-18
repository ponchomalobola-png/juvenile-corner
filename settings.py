import os

# Static files
STATIC_URL = '/static/'
STATIC_DIR = 'static'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_DIR = 'media'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ['juvenile-corner.onrender.com']
