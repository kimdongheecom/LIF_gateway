from app.domain.gateway.repositories.gateway_repository import OAuthRepository
from app.domain.gateway.models.gateway_model import OAuthEntity
from app.domain.gateway.schemas.gateway_schema import OAuthSchema, OAuthResponseSchema
import httpx
import os
import shortuuid
from datetime import datetime, timedelta
from typing import Optional, List


class OAuthService:
    """OAuth 인증 서비스 클래스"""
    
    def __init__(self):
        """서비스 초기화"""
        self.repository = OAuthRepository()
        
    async def initialize(self):
        """서비스 초기화 작업"""
        # 테이블 초기화
        await self.repository.init_table()
    
    async def get_oauth_by_id(self, id: str) -> Optional[OAuthEntity]:
        """ID로 OAuth 정보를 조회합니다"""
        return await self.repository.find_oauth_by_id(id)
    
    async def get_oauth_by_provider(self, provider: str) -> List[OAuthEntity]:
        """제공자별 OAuth 정보를 조회합니다"""
        return await self.repository.find_oauth_by_provider(provider)
    
    async def create_oauth(self, oauth_data: OAuthSchema) -> OAuthResponseSchema:
        """OAuth 인증 정보를 생성합니다"""
        provider = oauth_data.provider
        code = oauth_data.code
        redirect_uri = oauth_data.redirect_uri
        
        # 외부 OAuth 서비스에 토큰 요청
        token_response = await self._exchange_code_for_token(provider, code, redirect_uri)
        
        if not token_response or 'access_token' not in token_response:
            raise Exception(f"Failed to get token from {provider}")
        
        # 토큰 정보 저장
        oauth_entity = OAuthEntity(
            id=shortuuid.uuid(),
            provider=provider,
            access_token=token_response['access_token'],
            refresh_token=token_response.get('refresh_token'),
            expires_at=datetime.now() + timedelta(seconds=token_response.get('expires_in', 3600)),
            created_at=datetime.now()
        )
        
        # 저장
        await self.repository.save_oauth(oauth_entity)
        
        # 응답 생성
        return OAuthResponseSchema(
            access_token=oauth_entity.access_token,
            token_type="Bearer",
            expires_in=token_response.get('expires_in', 3600),
            refresh_token=oauth_entity.refresh_token,
            scope=token_response.get('scope'),
            created_at=oauth_entity.created_at
        )
    
    async def refresh_oauth_token(self, id: str) -> Optional[OAuthResponseSchema]:
        """토큰을 갱신합니다"""
        # 기존 토큰 조회
        oauth_entity = await self.repository.find_oauth_by_id(id)
        
        if not oauth_entity or not oauth_entity.refresh_token:
            return None
        
        # 리프레시 토큰으로 새 토큰 요청
        token_response = await self._refresh_token(
            oauth_entity.provider, 
            oauth_entity.refresh_token
        )
        
        if not token_response or 'access_token' not in token_response:
            return None
        
        # 토큰 정보 업데이트
        oauth_entity.access_token = token_response['access_token']
        if 'refresh_token' in token_response:
            oauth_entity.refresh_token = token_response['refresh_token']
        
        oauth_entity.expires_at = datetime.now() + timedelta(seconds=token_response.get('expires_in', 3600))
        
        # 저장
        await self.repository.save_oauth(oauth_entity)
        
        # 응답 생성
        return OAuthResponseSchema(
            access_token=oauth_entity.access_token,
            token_type="Bearer",
            expires_in=token_response.get('expires_in', 3600),
            refresh_token=oauth_entity.refresh_token,
            scope=token_response.get('scope'),
            created_at=oauth_entity.created_at
        )
    
    async def delete_oauth(self, id: str) -> bool:
        """OAuth 정보를 삭제합니다"""
        return await self.repository.delete_oauth(id)
    
    async def _exchange_code_for_token(self, provider: str, code: str, redirect_uri: Optional[str] = None) -> dict:
        """인증 코드를 토큰으로 교환합니다"""
        try:
            # 제공자별 토큰 엔드포인트 및 클라이언트 정보
            token_url, client_id, client_secret = self._get_provider_config(provider)
            
            # 토큰 요청 데이터
            data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'grant_type': 'authorization_code'
            }
            
            if redirect_uri:
                data['redirect_uri'] = redirect_uri
            
            # 토큰 요청
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data)
                
                if response.status_code != 200:
                    print(f"Error exchanging code for token: {response.text}")
                    return {}
                
                return response.json()
                
        except Exception as e:
            print(f"Error exchanging code for token: {e}")
            return {}
    
    async def _refresh_token(self, provider: str, refresh_token: str) -> dict:
        """리프레시 토큰으로 새 토큰을 요청합니다"""
        try:
            # 제공자별 토큰 엔드포인트 및 클라이언트 정보
            token_url, client_id, client_secret = self._get_provider_config(provider)
            
            # 토큰 갱신 요청 데이터
            data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token'
            }
            
            # 토큰 요청
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data)
                
                if response.status_code != 200:
                    print(f"Error refreshing token: {response.text}")
                    return {}
                
                return response.json()
                
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return {}
    
    def _get_provider_config(self, provider: str) -> tuple:
        """OAuth 제공자별 설정 정보를 가져옵니다"""
        if provider.lower() == 'google':
            return (
                'https://oauth2.googleapis.com/token',
                os.getenv('GOOGLE_CLIENT_ID', ''),
                os.getenv('GOOGLE_CLIENT_SECRET', '')
            )
        elif provider.lower() == 'facebook':
            return (
                'https://graph.facebook.com/v16.0/oauth/access_token',
                os.getenv('FACEBOOK_CLIENT_ID', ''),
                os.getenv('FACEBOOK_CLIENT_SECRET', '')
            )
        elif provider.lower() == 'github':
            return (
                'https://github.com/login/oauth/access_token',
                os.getenv('GITHUB_CLIENT_ID', ''),
                os.getenv('GITHUB_CLIENT_SECRET', '')
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")