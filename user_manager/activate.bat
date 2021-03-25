@REM set POSTGRES_DB_PORT=5432
@REM set POSTGRES_DB_USER_KEY=postgres
@REM set POSTGRES_DB_PASSWORD_KEY=Es#12390
@REM set POSTGRES_DB_HOST=qa-user-manager-rds.caneampnjecs.us-west-1.rds.amazonaws.com
@REM set POSTGRES_DB_NAME=postgres
set POSTGRES_DB_PORT=5432
set POSTGRES_DB_USER_KEY=postgres
set POSTGRES_DB_PASSWORD_KEY=12345
set POSTGRES_DB_HOST=127.0.0.1
set POSTGRES_DB_NAME=postgres

set ACCESS_TOKEN_KEY=C718D5FDDEC279567385BE3E52894
set REFRESH_TOKEN_KEY=9EA72AD96C39A87A1AFF153983592
set SMTP_USERNAME=AKIAXDMSSDW6WYN34VTV
set SMTP_PASSWORD=BIqBtf84NQ5jnpYKCeZcH0+/j7hXixGZmPW3X7PlTZeT
set SMTP_SERVER=email-smtp.us-west-1.amazonaws.com
set SMTP_PORT=587
set SMTP_FROM=elementapp@elementsci.com
set ADMIN_USERNAME=esadmin@elementsci.com
set ADMIN_PASSWORD=EleM3nTSci

@REM set OTP_EXPIRATION_TIME_HOURS=24
@REM set OTP_EXPIRATION_TIME_MINUTES=0
@REM set OTP_LIMIT=7
@REM set OTP_LIMIT_HOURS=1
@REM set OTP_LIMIT_MINUTES=0

set OTP_EXPIRATION_TIME_HOURS=0
set OTP_EXPIRATION_TIME_MINUTES=1
set OTP_LIMIT=7
set OTP_LIMIT_HOURS=0
set OTP_LIMIT_MINUTES=1



@REM python user_manager/app.py
@REM pytest -s -v -p no:warnings 
pytest -s -v -p no:warnings --cov=./user_manager --cov-report=html
@REM pytest ./test/ -s -v -p no:warnings
@REM py.test --cov=./user_manager --cov-report=html ALTERNET
@REM https://dba.stackexchange.com/questions/44586/forgotten-postgresql-windows-password