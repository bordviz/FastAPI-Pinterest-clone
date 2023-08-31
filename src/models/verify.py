from db.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from schemas.verify import VerifyRead

class Verify(Base):
    __tablename__ = 'verify'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True, nullable=False)
    code = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def to_read_model(self) -> VerifyRead:
        return VerifyRead(
            id=self.id,
            user_id=self.user_id,
            code=self.code,
            created_at=self.created_at,
            is_active=self.is_active
        )