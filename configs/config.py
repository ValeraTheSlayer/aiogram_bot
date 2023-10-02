import os

API_TOKEN = 'your_token'

DATABASE = {
    'dbname': os.environ.get('POSTGRES_DB', 'default_db_name'),
    'user': os.environ.get('POSTGRES_USER', 'default_user'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'default_password'),
    'host': os.environ.get('POSTGRES_HOST', 'default_host'),
    'port': os.environ.get('POSTGRES_PORT', 'default_port'),
}
