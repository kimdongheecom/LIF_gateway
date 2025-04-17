"""
Finance 라우터
- Finance 엔드포인트

"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

router = APIRouter(
    prefix="/finance",
    tags=["finance"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root() -> Dict[str, Any]:
    """
    Finance 서비스 루트 엔드포인트
    """
    return {"message": "Finance Service"} 