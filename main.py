# main.py
from fastapi import FastAPI
from dependencies.dependency import user_route
from dependencies.dependency import image_route
from dependencies.dependency import vote_route
from dependencies.dependency import auth_route

app = FastAPI()

app.include_router(auth_route.auth_router, tags=["auth"])
app.include_router(user_route.user_router, tags=["users"])
app.include_router(image_route.image_router, tags=["images"])
app.include_router(vote_route.vote_router,tags=["votes"])
