from fastapi import FastAPI
from .routers import github

app = FastAPI(
    title="Automation webhooks",
    description=""
)

app.include_router(github.router)
