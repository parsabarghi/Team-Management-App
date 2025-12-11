from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import settings
from routers.user_routers import router as user_router
from routers.auth_router import router as auth_router


from db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Starting Up...")
    await init_db()
    print("Tables Created Succesfully!")
    yield
    print("Application Shutting Down...")


app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def read_root():
    return {"root": "healthy"}