from email.policy import default
from sqlalchemy import Column, String, ForeignKey, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from models.Account import Account

class User(Account):
    __tablename__ = "user"
    
    account_id = Column(UUID(as_uuid=True), 
                        ForeignKey("account.id", 
                                   ondelete="CASCADE"), 
                        primary_key=True)
    
    first_name = Column(String)
    last_name = Column(String)
    image = Column(String, nullable=True)
    
    access_revoked = Column(BOOLEAN, default=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "user",
    }
    
    def __init__(self, password, email, first_name, last_name, image=None, type_account=None):
        super().__init__(password, email, type_account)
        self.first_name = first_name
        self.last_name = last_name
        self.image = image