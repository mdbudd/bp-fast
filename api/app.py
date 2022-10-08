import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import v0

rootPath = ""

if os.getenv("VCAP_APPLICATION"):
    rootPath = "/bp-fast"

description = """API Example"""

app = FastAPI(
    docs_url="/swag",
    redoc_url=None,
    root_path=rootPath,
    title="Example",
    description=description,
    version="0.0.1",
    terms_of_service="https://example.com/terms",
    contact={"name": "Matthew Budd", "url": "http://localhost:8000", "email": "matt@example.com"},
    license_info={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"},
)

app.include_router(v0.v0)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
