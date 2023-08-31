from db.db import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from schemas.post import PostRead

class Post(Base):
    __tablename__ = 'post'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    title = Column(String)
    subtitle = Column(String)
    image = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)

    def to_read_model(self) -> PostRead:
        return PostRead(
            id=self.id,
            title=self.title,
            subtitle=self.subtitle,
            image=self.image,
            likes=self.likes,
            user_id=self.user_id,
            created_at=self.created_at
        )