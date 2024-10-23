# Debe ir el codigo config de las conexiones con AWS ej: AWS_S3_ACCESS_KEY_ID, STORAGES = {} ...
# Recordar importar este archivo en el archivo base.py al final del codigo
# from config.settings.file_storage import *


# Configuracion para S3 ---------------------------------------------------------------------------------------------->
AWS_ACCESS_KEY_ID = 'AKIAUJ3VUNOLRMPT2SNY'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'bucket-r-projects'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'us-east-2'
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
