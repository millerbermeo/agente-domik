from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class OAuthConnection(Base):
    __tablename__ = 'oauth_connections'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    
    provider = Column(String, nullable=False)
    provider_account_id = Column(String)
    
    access_token = Column(String, nullable=False)
    refresh_token = Column(String)
    expiry_date = Column(DateTime)
    
    scopes = Column(String)
    extra_data = Column(JSON)
    
    user = relationship("User", back_populates="connections")