"""
Login 라우터
- Login 엔드포인트
- 토큰 관리
- 사용자 인증 처리
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root() -> Dict[str, Any]:
    """
    Login 서비스 루트 엔드포인트
    """
    return {"message": "Login Service"} 