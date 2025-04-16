# Gateway API

www.jinmini.com 도메인을 위한 게이트웨이 API 서버입니다.

## 기술 스택

- FastAPI
- Docker
- Python 3.12.7
- AsyncPG
- SQLAlchemy

## 실행 방법

### Docker Compose 사용

```bash
docker-compose up --build
```

### 직접 실행

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

## API 문서

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## 환경 변수

`.env` 파일에 다음 환경 변수를 설정합니다:

- DOMAIN: 도메인 주소 (기본값: www.jinmini.com)
- PORT: 서버 포트 (기본값: 8080) 