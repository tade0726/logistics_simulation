

DATABASES_DIC = {
    'LOCAL': {
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root123',
        'NAME': 'hangzhouhubqa_v3',
        'CHARSET': 'utf8'
    },
    'TEST': {
        'HOST': '10.0.149.62',
        'USER': 'root',
        'PASSWORD': 'root123',
        'NAME': 'cloud_mirror_v1',
        'CHARSET': 'utf8'
    },
    'PRODUCTION': {

    }
}
DATABASES = DATABASES_DIC['TEST']
