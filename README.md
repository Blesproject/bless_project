# COCKROACH BOILERPLATE WITH JWT PROJECT


## Environment File

``` bash
APP_NAME = Cockroach Boilerplate
APP_HOST = 127.0.0.1
APP_PORT = 5000
SECRET_KEY = YOUR SECRET

MEMCACHE_HOST=127.0.0.1
MEMCACHE_PORT=11211

FLASK_DEBUG = True
FLASK_REDIS_URL = redis://:pass@127.0.0.1:6379/0

JWT_SECRET_KEY = YOUR SECRET

DB_NAME = db
DB_HOST = localhost
DB_PORT = 26257
DB_USER = root
DB_SSL = disable

SWAGGER_URL = '/api/docs'
SWAGGER_API_URL = 'http://petstore.swagger.io/v2/swagger.json'
```

move env.local to .env


## Local Development

Installing Requirements
``` bash
pip install -r requirements.txt
```

run server
``` bash
python manage.py server
```

## Documentation

See Documentation in http://host/api/docs  see swagger url in .env file or If Using Postman Open DOCS Folder import
