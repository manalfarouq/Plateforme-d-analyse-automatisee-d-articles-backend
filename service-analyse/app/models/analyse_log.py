# service-analyse/app/models/analyse_log.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .user import Base


class AnalyseLog(Base):
    __tablename__ = "analyse_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    texte_original = Column(Text, nullable=False)
    categorie = Column(String(100), nullable=False)
    resume = Column(Text, nullable=True)
    ton = Column(String(50), nullable=True)
    
    # Relation avec User
    user = relationship("User", back_populates="analyse_logs")