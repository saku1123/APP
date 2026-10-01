passwd codespace "student"

# 1. 重置資料庫
PGPASSWORD='student' psql -U vtc_user -d vtc_sas -h localhost -c "DROP TABLE IF EXISTS users CASCADE; DROP TYPE IF EXISTS user_role_enum; DROP TYPE IF EXISTS gender_enum;"

# 2. 啟動 Uvicorn
uvicorn main:app --reload --port 8000
https://stunning-zebra-966qjrr9jjqhppg5-8000.app.github.dev/docs
