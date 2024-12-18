# Debe ir el codigo config de las conexiones con AWS ej: AWS_S3_ACCESS_KEY_ID, STORAGES = {} ...
# Recordar importar este archivo en el archivo base.py al final del codigo
# from config.settings.file_storage import *
import os
from config.env import BASE_DIR, env
env.read_env(os.path.join(BASE_DIR, '.env'))

# Configuracion para S3 ---------------------------------------------------------------------------------------------->
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = env('AWS_S3_SIGNATURE_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERIFY = True

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
