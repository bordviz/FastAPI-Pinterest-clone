from pydantic import BaseModel
from .config import TunedModel

class SubscriptionCreate(BaseModel):
    subscriber: int
    account: int

class SubscriptionRead(TunedModel):
    id: int
    subscriber: int
    account: int