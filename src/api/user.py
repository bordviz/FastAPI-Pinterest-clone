from typing import List
from fastapi import APIRouter, File, UploadFile
from schemas.user import UserProfile, UserRead
from schemas.subscription import SubscriptionCreate
from .dependencies import CurrentUser, UOWDep, VerifiedUser
from services.user import UserService

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/profile', status_code=200, response_model=UserProfile)
async def get_user_profile(
    uow: UOWDep,
    user: CurrentUser
):
    profile = await UserService().get_user_profile(uow, user)
    return profile

@router.post('/subscribe', status_code=200)
async def subscribe(
    data: SubscriptionCreate,
    uow: UOWDep
):
    res = await UserService().subscribe(uow, data)
    return res

@router.post('/unsubscribe', status_code=200)
async def unsubscribe(
    data: SubscriptionCreate,
    uow: UOWDep
):
    res = await UserService().unsubscribe(uow, data)
    return res

@router.patch('/update-avatar', status_code=200)
async def update_avatar(
    user: VerifiedUser,
    uow: UOWDep,
    image: UploadFile = File(...)
):
    res = await UserService().update_avatar(uow, user, image)
    return res

@router.delete('/delete-avatar', status_code=200)
async def delete_avatar(
    user: VerifiedUser,
    uow: UOWDep,
):
    res = await UserService().delete_avatar(uow, user)
    return res

@router.get('/get-subscriptions/{id}', status_code=200, response_model=List[UserRead])
async def get_user_subscriptions(
    id: int,
    uow: UOWDep
):
    res = await UserService().get_user_subscriptions(uow, id)
    return res

@router.get('/get-subscribers/{id}', status_code=200, response_model=List[UserRead])
async def get_user_subscriptions(
    id: int,
    uow: UOWDep
):
    res = await UserService().get_user_subscribers(uow, id)
    return res

@router.get('{id}', status_code=200, response_model=UserProfile)
async def get_user_by_id(
    id: int,
    uow: UOWDep
):
    user = await UserService().get_user_by_id(uow, id)
    return user