from fastapi import FastAPI


async def lifespan(_app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
