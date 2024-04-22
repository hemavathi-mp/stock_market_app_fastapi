import os

from fastapi import APIRouter, Depends, Request, FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from task.models import model as Register
from task.routers import task_router
from task.config.db import engine, SessionLocal, get_db

Register.DB_BASE.metadata.create_all(bind=engine)
# ld.DB_BASE.metadata.create_all(bind=engine)
task = FastAPI(
    title="New_Task",
    description="API's for New Task",
    version="1.0.0",
    proxy_headers=True,  # THIS LINE
    forwarded_allow_ips='*',  # THIS LINE
)

load_dotenv()  # take environment variables from .env.
SOME_CONFIG_I_NEED = os.environ.get("SOME_CONFIG_I_NEED")

origins = ["*"]
methods = ["*"]

task.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],

)

task.include_router(task_router.router)

