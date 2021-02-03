In env file include_schemas=True,

To migrate the Model Schema to database
1. flask db init(only to generate the migration folder)
2. flask db migrate -m "message"
3. flask db upgrade


To run Application
1. create a virtual env using command python venv <env_name>
2. copy this command in activate.bat file
set POSTGRES_DB_PORT=value
set POSTGRES_DB_USER_KEY=value
set POSTGRES_DB_PASSWORD_KEY=value
set POSTGRES_DB_HOST=value
set POSTGRES_DB_NAME=value

set ACCESS_TOKEN_KEY=value
set REFRESH_TOKEN_KEY=value

set SMTP_USERNAME=value
set SMTP_PASSWORD=value
set SMTP_SERVER=value
set SMTP_PORT=value
set SMTP_FROM=value
set SMTP_FROM=value
3. Activate the virtual env using cd/env_name/Scripts/activate.bat(for window user)
4. python app.py (For application up)