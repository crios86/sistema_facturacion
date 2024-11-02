class Config:
    SECRET_KEY = 'betgames3x'


class DevelopmentConfig(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = True
    MYSQL_HOST = 'junction.proxy.rlwy.net'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'WRnKKzyTMoQRYpBUUeNcPQrdnuGWFaOZ'
    MYSQL_DB = 'railway'
    MYSQL_PORT = 23625  # Puerto de la instancia

# Configuración del entorno
config = {
    'development': DevelopmentConfig
}

