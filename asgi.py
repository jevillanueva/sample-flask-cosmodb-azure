import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from app import app
config = Config()
config.bind = ["0.0.0.0:5000"]
asyncio.run(serve(app, config=config))
