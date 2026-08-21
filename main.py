from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import user_router, event_router, role_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(event_router)
app.include_router(role_router)
