from .auth import router as router_auth
from .user import router as router_user
from .verify import router as router_verify
from .image import router as router_image
from .post import router as router_post

all_routers = [
    router_auth,
    router_verify,
    router_user,
    router_image,
    router_post
]
