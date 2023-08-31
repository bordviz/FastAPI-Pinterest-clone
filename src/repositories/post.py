from utils.repository import SQLAlchemyRepository
from models.post import Post

class PostRepository(SQLAlchemyRepository):
    model = Post