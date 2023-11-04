# Should be set to "production" for production environment
ENV = 'development'

SECRET_KEY = 'dev'
SQLALCHEMY_DATABASE_URI = 'postgresql://belka:belka@localhost:5432/belka'
SESSION_PROTECTION = 'strong'
