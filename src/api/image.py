from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(
    prefix='/image',
    tags=['Image']
)

@router.get('/{name}')
async def hello(
    name: str
):
    return FileResponse(f'../images/{name}.jpg')
