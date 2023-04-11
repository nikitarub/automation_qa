from .webhooks_app import app
import uvicorn
import asyncio


async def run_webhook():
    config = uvicorn.Config(app, port=3000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
