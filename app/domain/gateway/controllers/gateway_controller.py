from fastapi import APIRouter, HTTPException, Query
from app.domain.gateway.services.gateway_service import OAuthService
from app.domain.gateway.schemas.gateway_schema import OAuthSchema, OAuthResponseSchema
from app.domain.gateway.models.gateway_model import OAuthEntity
from typing import List

router = APIRouter()
oauth_service = OAuthService()

@router.get("/oauth/{oauth_id}", response_model=OAuthEntity)
async def get_oauth_by_id(oauth_id: str):
    """ID로 OAuth 정보 조회"""
    oauth = await oauth_service.get_oauth_by_id(oauth_id)
    if not oauth:
        raise HTTPException(status_code=404, detail="OAuth 정보를 찾을 수 없습니다")
    return oauth

@router.get("/oauth", response_model=List[OAuthEntity])
async def get_oauth_by_provider(provider: str = Query(..., description="OAuth 제공자")):
    """제공자별 OAuth 정보 조회"""
    return await oauth_service.get_oauth_by_provider(provider)

@router.post("/oauth", response_model=OAuthResponseSchema)
async def create_oauth(oauth_data: OAuthSchema):
    """OAuth 인증 정보 생성"""
    try:
        return await oauth_service.create_oauth(oauth_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/oauth/{oauth_id}/refresh", response_model=OAuthResponseSchema)
async def refresh_oauth_token(oauth_id: str):
    """OAuth 토큰 갱신"""
    response = await oauth_service.refresh_oauth_token(oauth_id)
    if not response:
        raise HTTPException(status_code=404, detail="토큰 갱신에 실패했습니다")
    return response

@router.delete("/oauth/{oauth_id}", response_model=bool)
async def delete_oauth(oauth_id: str):
    """OAuth 정보 삭제"""
    result = await oauth_service.delete_oauth(oauth_id)
    if not result:
        raise HTTPException(status_code=404, detail="OAuth 정보를 찾을 수 없습니다")
    return True
