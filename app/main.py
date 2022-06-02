from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .routers import post, user, vote, auth

# Creates all the db tables by the models when the app first runs\
# Isnt needed anymore since we started using alembic as db migration tool
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Adds the post and user routes to the main app router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

# CORS logic
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to my API =]"}
