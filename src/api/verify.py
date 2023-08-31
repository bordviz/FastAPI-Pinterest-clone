from fastapi import APIRouter, Request
from services.verify import VerifyService
from .dependencies import UOWDep
from schemas.verify import VerifyCreate

router = APIRouter(
    prefix='/verify',
    tags=['Verify']
)

@router.post('/get-mail{user_id}')
async def get_verify_mail(
    user_id: int,
    uow: UOWDep
):
    res = await VerifyService().get_verify_code(uow, user_id)
    return res

@router.post('/send-code')
async def send_verify_code(
    data: VerifyCreate,
    uow: UOWDep
):
    res = await VerifyService().send_verify_code(uow, data)
    return res
