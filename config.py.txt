import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # MercadoPago (Producción)
    MP_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN')
    
    # Google Sheets API (Tu URL actual)
    GOOGLE_SCRIPT_URL = os.getenv('GOOGLE_SCRIPT_URL', 
        "https://script.google.com/macros/library/d/1I6G4hoPgOZVoypp5SzBntSdrjZ76mY9fscWHPnjgy-5SX4bYgSmaRE0u/7")
    
    # Database (Render PostgreSQL)
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Admin
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
    
    # Business Config
    BUSINESS_NAME = "TCG Pet Store"
    BRANDS = ["Master Crock", "Upper Crock"]
    DESCUENTO_EFECTIVO = 0.10
    DESCUENTO_TRANSFERENCIA = 0.05
    COSTO_ENVIO_MOTO = 2500
    COSTO_ENVIO_DELIVERY = 1800
    ENVIO_GRATIS_MINIMO = 50000

config = Config()
