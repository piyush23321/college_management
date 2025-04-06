from auth import login
from routers import controllers
from config import configuration
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from database.db_connection import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables (if not exists)...")
    create_db_and_tables()  # Runs ONCE when the app starts
    yield  # Application runs after this
    print("Application shutting down...")  # (Optional) Cleanup logic here


# App
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.co.uk"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include Routers
app.include_router(configuration.router, prefix="/api", tags=["config"])
app.include_router(controllers.router, tags=["College"])
app.include_router(login.router, tags=["Login"])



# Steps to upgrdae
# [1] alembic revision --autogenerate -m "initial migration"
# [2] alembic upgrade head 
