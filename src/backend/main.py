import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import setup_cache
from di import lifespan
from routers import example_router


def main() -> FastAPI:
    app = FastAPI(
        debug=bool(int(os.environ["DEBUG"])),
        title=os.environ["APP_NAME"],
        root_path="/api",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    # app.include_router(example_router.router)
    setup_cache()
    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:main",
        factory=True,
        host="0.0.0.0",
        port=8000,
        workers=2,
        limit_concurrency=500,
        limit_max_requests=10000,
        reload=bool(int(os.environ["DEBUG"])),
    )
