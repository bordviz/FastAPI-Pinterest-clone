from schemas.post import PostCreate, PostSend
from schemas.user import UserRead
from utils.unitofwork import IUnitOfWork
from fastapi import HTTPException, UploadFile
from config import IMAGE_PLACEHOLDER
from models.post import Post
from models.user import User
from sqlalchemy import or_

class PostService:
    async def upload_post_image(self, uow: IUnitOfWork, user: UserRead, file: UploadFile):
        async with uow:
            image_type = file.filename.split('.')[1].lower()
            if image_type != 'png' and image_type != 'jpg' and image_type != 'jpeg':
                await uow.rollback()
                raise HTTPException(status_code=400, detail='Invalid image format, available formats: jpg, jpeg, png')
            if file.size > 5000000:
                await uow.rollback()
                raise HTTPException(status_code=400, detail='File size larger than 5mb')
            posts = await uow.post.get_all(user_id=user.id)
            with open(f'../images/{user.id}_{len(posts)+1}.jpg', 'wb') as f:
                f.write(file.file.read())
            return {
                'status': 'success',
                'image_path': f'{IMAGE_PLACEHOLDER}/image/{user.id}_{len(posts)+1}'
            }

    async def create_post(self, uow: IUnitOfWork, data: PostCreate):
        async with uow:
            res = await uow.post.add_one(data.model_dump())
            if not res:
                await uow.rollback()
                raise HTTPException(status_code=400)
            await uow.commit()
            return {
                'status': 'success',
                'message': f'A new post with id {res} was successfully created'
            }
        
    async def get_post_by_id(self, uow: IUnitOfWork, id: int):
        async with uow:
            post = await uow.post.get_one(id=id)
            if not post:
                await uow.rollback()
                raise HTTPException(status_code=404, detail='Post not found')
            user = await uow.user.get_one(id=post.user_id)
            res = PostSend(
                **post.model_dump(),
                user=user
            )
            return res
        
    async def add_like_to_post(self, uow: IUnitOfWork, id: int):
        async with uow:
            post = await uow.post.get_one(id=id)
            if not post:
                await uow.rollback()
                raise HTTPException(status_code=404, detail='Post not found')
            res = await uow.post.update(where=[Post.id == id], values={'likes': post.likes+1})
            return {
                'status': 'success',
                'message': f'Add like to post {res}'
            }
    
    async def get_posts(self, uow: IUnitOfWork, limit: int, start: int):
        async with uow:
            res = await uow.post.join(
                target=User,
                onclause=Post.user_id == User.id, 
                start=start, 
                limit=limit, 
                order_by=Post.created_at.desc())
            final_res = []
            for i in res:
                post = i[0].to_read_model().model_dump()
                user = i[1].to_read_model()
                final_res.append(PostSend(**post, user=user))
            return final_res
        
    async def search_posts(self, uow:IUnitOfWork, query: str, limit: int, start: int):
        async with uow:
            res = await uow.post.join(
                target=User,
                onclause=Post.user_id == User.id, 
                where=[or_(
                    Post.title.like(f'%{query.lower()}%'), Post.title.like(f'%{query.upper()}%'), Post.title.like(f'%{query.title()}%'),  
                    Post.subtitle.like(f'%{query.lower()}%'), Post.subtitle.like(f'%{query.upper()}%'), Post.subtitle.like(f'%{query.title()}%'), 
                    User.username.like(f'%{query.lower()}%'), User.username.like(f'%{query.upper()}%'), User.username.like(f'%{query.title()}%')
                    )],
                start=start, 
                limit=limit, 
                order_by=Post.created_at.desc())
            final_res = []
            for i in res:
                post = i[0].to_read_model().model_dump()
                user = i[1].to_read_model()
                final_res.append(PostSend(**post, user=user))
            return final_res
