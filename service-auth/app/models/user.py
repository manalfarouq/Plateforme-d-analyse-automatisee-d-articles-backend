# service-auth/app/models/user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    createat = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relation avec AnalyseLog (utiliser string pour éviter l'import circulaire)
    analyse_logs = relationship("AnalyseLog", back_populates="user", lazy="dynamic")