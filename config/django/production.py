from .base import *
from config.env import env

DEBUG = env.bool('DJANGO_DEBUG', default = False)

CSRF_TRUSTED_ORIGINS = env.list(
    'CSRF_TRUSTED_ORIGINS', 
    default=[]
)

ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS', 
    default = []
)