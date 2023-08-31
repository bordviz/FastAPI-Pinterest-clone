from utils.repository import SQLAlchemyRepository
from models.subscription import Subscription

class SubscriptionRepository(SQLAlchemyRepository):
    model = Subscription