from typing import Any, Dict
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import httpx
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from app.api.gateway.tokens_router import router as tokens_router
from app.api.gateway.finance_router import router as finance_router
from app.api.gateway.esg_router import router as esg_router
from app.api.gateway.login_router import router as login_router




# .env 파일 로드
load_dotenv()



# ✅ FastAPI 앱 생성 
app = FastAPI(
    title="Gateway API",
    description="Gateway API for jinmini.com",
    version="0.1.0",

)
gateway_router = APIRouter(prefix="/e")



# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_URL")

if not GATEWAY_SERVICE_URL:
    raise ValueError("GATEWAY_SERVICE_URL environment variable is not set")


# ✅ 애플리케이션 시작 시 `init_db()` 실행
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀🚀🚀🚀 FastAPI 앱이 시작됩니다. 데이터베이스 초기화 중...")
    # await init_db()  # ✅ DB 초기화 실행
    # print("✅ 데이터베이스 초기화 완료!")
    yield  # 애플리케이션이 실행되는 동안 유지
    print("🛑 FastAPI 앱이 종료됩니다.")

app.include_router(gateway_router)


# tokens_router 등록 (최종 경로가 /e/tokens이 되도록 설정)
app.include_router(tokens_router, prefix="/e")

# login_router 등록 (최종 경로가 /e/login이 되도록 설정)
app.include_router(login_router, prefix="/e")

# esg_router 등록 (최종 경로가 /e/esg이 되도록 설정)
app.include_router(esg_router, prefix="/e")

# finance_router 등록 (최종 경로가 /e/finance이 되도록 설정)
app.include_router(finance_router, prefix="/e")


# ✅ 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 