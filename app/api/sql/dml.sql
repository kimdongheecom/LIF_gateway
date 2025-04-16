INSERT INTO users (email, username, hashed_password, role, is_active)
VALUES (
  'alice@example.com',
  'Alice',
  '$2b$12$Lk6z2mDfGweqtWdCwWHlqa.N2/QNucA1Ey2FRRDmd3yX4Bf75Jz6f',  -- 해시값
  'user',
  true
);