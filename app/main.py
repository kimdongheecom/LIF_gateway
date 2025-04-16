from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import httpx
import os
from dotenv import load_dotenv

from app.domain.gateway.controllers.gateway_controller import router as gateway_router
from app.domain.gateway.services.gateway_service import OAuthService

# .env 파일 로드
load_dotenv()

# ✅ OAuthService 인스턴스 생성
oauth_service = OAuthService()

# ✅ lifespan 함수 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    await oauth_service.initialize()  # 앱 시작 시 테이블 초기화
    yield  # (앱 종료 시 정리 로직이 필요하면 여기에 추가)

# ✅ FastAPI 앱 생성 (lifespan 적용)
app = FastAPI(
    title="Gateway API",
    description="Gateway API for jinmini.com",
    version="0.1.0",
    lifespan=lifespan
)

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 루트 경로 핸들러
@app.get("/")
async def root():
    return {"message": "Welcome to jinmini.com Gateway API"}

@gateway_router.get("/")
async def hello_world():
    return {"message": "Hello World"}

@gateway_router.get("/health")
async def health_check():
    return {"status": "healthy"}

# ✅ auth 프록시 경로 직접 등록
@app.api_route("/e/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def auth_proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        auth_service_url = os.getenv("AUTH_SERVICE_URL")
        if not auth_service_url:
            raise Exception("AUTH_SERVICE_URL이 .env 파일에 설정되지 않았습니다.")
        
        url = f"{auth_service_url}/{path}"
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)
        
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            params=request.query_params
        )
        return JSONResponse(
            content=response.json(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

# ✅ Gateway Router 등록 (/e로 prefix 고정)
app.include_router(gateway_router, prefix="/e")

# ✅ 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 