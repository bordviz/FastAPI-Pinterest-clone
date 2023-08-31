from abc import ABC, abstractmethod
from db.db import AsyncSession
from sqlalchemy import ColumnExpressionArgument, select, insert, update, delete

class AbstractRepository(ABC):

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_where(self):
        raise NotImplementedError
    
    @abstractmethod
    async def get_one(self):
        raise NotImplementedError
    
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self):
        raise NotImplementedError
    
    @abstractmethod
    async def join(self):
        raise NotImplementedError
    
class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__ (self, session: AsyncSession):
        self.session = session

    async def get_all(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
    
    async def get_all_where(self, where: ColumnExpressionArgument[bool], limit: int = None):
        stmt = select(self.model).where(*where).limit(limit)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
    
    async def get_one(self, full_model: bool = False, **filter_by):
        try:
            stmt = select(self.model).filter_by(**filter_by).limit(1)
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            if not full_model:
                res = res.to_read_model()
            return res
        except:
            return None
        
    async def add_one(self, data: dict):
        try:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res_id = await self.session.execute(stmt)
            return res_id.scalar_one()
        except:
            return None
    
    async def update(self, where: ColumnExpressionArgument[bool], values: dict):
        try:
            stmt = update(self.model).where(*where).values(**values).returning(self.model.id)
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except:
            return None
        
    async def delete(self, **filter_by):
        try:
            stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(stmt)
            return True
        except:
            return None
        
    async def join(self, target, onclause = None, where: ColumnExpressionArgument[bool] = [], start: int = 0, limit: int = 50, order_by = None):
        stmt = select(self.model, target).join(target, onclause).where(*where).offset(start).limit(limit).order_by(order_by)
        print(stmt)
        res = await self.session.execute(stmt)
        res = [row for row in res.all()]
        return res

