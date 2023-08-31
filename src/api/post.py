from fastapi import APIRouter, Body
from .dependencies import UOWDep, VerifiedUser
from schemas.post import PostCreate
from fastapi import UploadFile, File
from services.post import PostService
from typing import Annotated

router = APIRouter(
    prefix='/post',
    tags=['Post']
)

@router.post('/upload-file', status_code=200)
async def upload_post_file(
    uow: UOWDep,
    user: VerifiedUser,
    file: UploadFile = File(...)
):
    res = await PostService().upload_post_image(uow, user, file)
    return res

@router.post('/create', status_code=200)
async def create_post(
    uow: UOWDep,
    user: VerifiedUser,
    data: PostCreate
):
    data.user_id = user.id
    res = await PostService().create_post(uow, data)
    return res

@router.post('/like/{post_id}')
async def add_like_to_post(
    post_id: int,
    user: VerifiedUser,
    uow: UOWDep
):
    res = await PostService().add_like_to_post(uow, post_id)
    return res

@router.post('/search', status_code=200)
async def search_posts(
    uow: UOWDep,
    limit: int = 50,
    start: int = 0,
    query: str = Body(...)
):
    res = await PostService().search_posts(uow, query, limit, start)
    return res

@router.get('/', status_code=200)
async def get_posts(
    uow: UOWDep,
    limit: int = 50,
    start: int = 0,
):
    res = await PostService().get_posts(uow, limit, start)
    return res

@router.get('/{id}', status_code=200)
async def get_post_by_id(
    id: int,
    user: VerifiedUser,
    uow: UOWDep
):
    res = await PostService().get_post_by_id(uow, id)
    return res
