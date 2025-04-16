CREATE TABLE users (
    user_id VARCHAR(15) PRIMARY KEY,
    email VARCHAR(20) UNIQUE NOT NULL,
    hashed_password VARCHAR(15) NOT NULL,
    name VARCHAR(10) NOT NULL
);
#postgres에서 users테이블 생성
