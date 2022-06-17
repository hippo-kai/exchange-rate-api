from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response, JSONResponse
import time

from app.routers import exchange_rates

load_dotenv()

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({ 'message': str(exc.detail) }, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({ 'message': str(exc) }, status_code=400)


@app.middleware('http')
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get('/health')
def root():
    return {'message': 'OK'}

app.include_router(exchange_rates.router)