from fastapi import APIRouter
from .endpoints import translate  ,root

app_router = APIRouter()

app_router.get("/")(root) 

app_router.post("/translate")(translate)