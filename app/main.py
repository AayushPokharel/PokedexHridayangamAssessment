from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from database import load_db_with_pokemons, get_db_connection
from v1.urls import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_db_connection()
    await load_db_with_pokemons()
    yield


static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(v1_router, prefix="/api/v1")
