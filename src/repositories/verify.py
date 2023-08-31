from utils.repository import SQLAlchemyRepository
from models.verify import Verify

class VerifyRepository(SQLAlchemyRepository):
    model = Verify