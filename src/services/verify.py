from utils.unitofwork import IUnitOfWork
from random import randint
from models.verify import Verify
from models.user import User
from schemas.verify import VerifyCreate, VerifyRead
from utils.worker import send_email_code
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from datetime import datetime, timedelta

class VerifyService:
    async def get_verify_code(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            user = await uow.user.get_one(id=user_id)
            if user.is_verified:
                await uow.rollback()
                raise HTTPException(status_code=403, detail='User is already verified')
            check = await uow.verify.get_one(user_id=user_id)
            if check:
                await uow.verify.update([Verify.user_id == user_id, Verify.is_active == True], {'is_active': False})
            code = randint(100000, 999999)
            model = VerifyCreate(user_id=user_id, code=code)
            await uow.verify.add_one(model.model_dump())
            await uow.commit()
            send_email_code.delay(user.username, user.email, code)
            return {
                'status': 'success',
                'message': 'A letter with verification code was sent to the user\'s mailbox'
            }
    
    async def send_verify_code(self, uow: IUnitOfWork, data: VerifyCreate):
        try:
            async with uow:
                verify: VerifyRead= await uow.verify.get_one(user_id=data.user_id, is_active=True)
                if verify.code != data.code:
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='Incorrect code')
                limit_time = datetime.utcnow()
                created_time = verify.created_at + timedelta(minutes=10)
                if created_time.timestamp() < limit_time.timestamp():
                    await uow.rollback()
                    raise HTTPException(status_code=400, detail='Incorrect code')
                res = await uow.user.update(where=[User.id == verify.user_id], values={'is_verified': True})
                await uow.verify.update([Verify.user_id == verify.user_id, Verify.is_active == True], {'is_active': False})
                await uow.commit()
                return {
                    'status': 'success',
                    'message': f'User {res} successfully verified'
                }
        except NoResultFound:
            raise HTTPException(status_code=404, detail='Code not found')
