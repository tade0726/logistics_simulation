

DATABASES_DIC = {
    'LOCAL': {
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'gsvc123456',
        'NAME': 'hangzhouhubland',
        'CHARSET': 'utf8'
    },
    'TEST': {
        'HOST': '10.0.149.62',
        'USER': 'root',
        'PASSWORD': 'root123',
        'NAME': 'hangzhouhubqa_2',
        'CHARSET': 'utf8'
    },
    'PRODUCTION': {

    }
}
DATABASES = DATABASES_DIC['TEST']
