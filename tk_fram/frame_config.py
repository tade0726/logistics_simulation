

DATABASES_DIC = {
    'LOCAL': {
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'root123',
        'NAME': 'hangzhouhubqa_v3',
        'CHARSET': 'utf8'
    },
    'TEST': {
        'HOST': '10.0.149.36',
        'USER': 'wenjing',
        'PASSWORD': 'wenjing',
        'NAME': 'hangzhouhubqa_v3',
        'CHARSET': 'utf8'
    },
    'PRODUCTION': {

    }
}
DATABASES = DATABASES_DIC['TEST']
