from db.db import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from schemas.subscription import SubscriptionRead

class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, unique=True)
    subscriber = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    account = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)

    def to_read_model(self) -> SubscriptionRead:
        return SubscriptionRead(
            id=self.id,
            subscriber=self.subscriber,
            account=self.account
        )
