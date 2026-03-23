from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from config import config

Base = declarative_base()

class PedidoDB(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True)
    pedido_id = Column(String(50), unique=True, nullable=False)
    telegram_id = Column(String(50), nullable=False)
    cliente_nombre = Column(String(100))
    items = Column(Text)
    total = Column(Float)
    estado = Column(String(20), default='pendiente')
    metodo_pago = Column(String(20))
    mp_payment_id = Column(String(50))
    fecha_creacion = Column(DateTime, default=datetime.now)

def init_db():
    engine = create_engine(config.DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine
