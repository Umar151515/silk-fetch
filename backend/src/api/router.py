from fastapi import APIRouter

from backend.src.api.v1 import router as router_v1


router = APIRouter(prefix="/api")

router.include_router(router_v1)