import os
from typing import List
from utils.unitofwork import IUnitOfWork
from fastapi import HTTPException
from schemas.user import UserRead, UserProfile
from schemas.subscription import SubscriptionCreate, SubscriptionRead
from models.user import User
from fastapi import UploadFile
from config import IMAGE_PLACEHOLDER

class UserService:
    async def get_user_profile(self, uow: IUnitOfWork, user: UserRead):
        async with uow:
            posts = await uow.post.get_all(user_id=user.id)
            user_profile = UserProfile(**user.model_dump(), posts=posts)
            return user_profile

    async def get_user_by_id(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            user = await uow.user.get_one(id=user_id)
            if not user:
                await uow.rollback()
                raise HTTPException(status_code=404, detail='User not found')
            posts = await uow.post.get_all(user_id=user.id)
            user_profile = UserProfile(**user.model_dump(), posts=posts)
            return user_profile
        
    async def subscribe(self, uow: IUnitOfWork, data: SubscriptionCreate):
        async with uow:
            try:
                check = await uow.subscription.get_one(subscriber=data.subscriber, account=data.account)
                if check:
                    await uow.rollback()
                    raise
                await uow.subscription.add_one(data.model_dump())
                account = await uow.user.get_one(id=data.account)
                user = await uow.user.get_one(id=data.subscriber)
                await uow.user.update(where=[User.id==data.account], values={'subscribers': account.subscribers + 1})
                await uow.user.update(where=[User.id==data.subscriber], values={'subscriptions': user.subscriptions + 1})
                await uow.commit()
                return {
                    'status': 'success',
                    'message': 'You have successfully subscribe to the user'
                }
            except HTTPException as err:
                raise HTTPException(status_code=err.status_code)
            except:
                await uow.rollback()
                raise HTTPException(status_code=400)

    async def unsubscribe(self, uow: IUnitOfWork, data: SubscriptionCreate):
        async with uow:
            try:
                check = await uow.subscription.get_one(subscriber=data.subscriber, account=data.account)
                if not check:
                    await uow.rollback()
                    raise HTTPException(status_code=404)
                await uow.subscription.delete(subscriber=data.subscriber, account=data.account)
                account = await uow.user.get_one(id=data.account)
                user = await uow.user.get_one(id=data.subscriber)
                await uow.user.update(where=[User.id==data.account], values={'subscribers': account.subscribers - 1})
                await uow.user.update(where=[User.id==data.subscriber], values={'subscriptions': user.subscriptions - 1})
                await uow.commit()
                return {
                    'status': 'success',
                    'message': 'You have successfully unsubscribed from a user'
                }
            except HTTPException as err:
                raise HTTPException(status_code=err.status_code)
            except:
                await uow.rollback()
                raise HTTPException(status_code=400)

    async def get_user_subscriptions(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            res: List[SubscriptionRead] = await uow.subscription.get_all(subscriber=user_id)
            if res == []:
                return []
            accounts = [row.account for row in res]
            subscriptions = await uow.user.get_all_where(where=[User.id.in_(accounts)])
            return subscriptions
        
    async def get_user_subscribers(self, uow: IUnitOfWork, user_id: int):
        async with uow:
            res: List[SubscriptionRead] = await uow.subscription.get_all(account=user_id)
            if res == []:
                return []
            users = [row.subscriber for row in res]
            subscribers= await uow.user.get_all_where(where=[User.id.in_(users)])
            return subscribers
        
    async def update_avatar(self, uow: IUnitOfWork, user: UserRead, file: UploadFile):
        async with uow:
            image_type = file.filename.split('.')[1].lower()
            if image_type != 'png' and image_type != 'jpg' and image_type != 'jpeg':
                await uow.rollback()
                raise HTTPException(status_code=400, detail='Invalid image format, available formats: jpg, jpeg, png')
            if file.size > 5000000:
                await uow.rollback()
                raise HTTPException(status_code=400, detail='File size larger than 5mb')
            with open(f'../images/user-avatar-{user.id}.jpg', 'wb') as f:
                f.write(file.file.read())
            await uow.user.update(where=[User.id == user.id], values={'avatar_image': f'{IMAGE_PLACEHOLDER}/image/user-avatar-{user.id}'})
            await uow.commit()
            return {
                'status': 'success',
                'message': 'Profile avatar successfully updated'
            }
        
    async def delete_avatar(self, uow: IUnitOfWork, user: UserRead):
        async with uow:
            if not user.avatar_image:
                await uow.rollback()
                raise HTTPException(status_code=400)
            os.remove(f'../images/user-avatar-{user.id}.jpg')
            await uow.user.update(where=[User.id == user.id], values={'avatar_image': None})
            await uow.commit()
            return {
                'status': 'success',
                'message': 'Profile avatar successfully deleted'
            }