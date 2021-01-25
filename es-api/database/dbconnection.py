# database connection
import os

def getConString():
    host = os.environ.get('POSTGRES_DB_HOST')
    port = os.environ.get('POSTGRES_DB_PORT')
    database_name = os.environ.get('POSTGRES_DB_NAME')
    user = os.environ.get('POSTGRES_DB_USER_KEY')
    password = os.environ.get('POSTGRES_DB_PASSWORD_KEY')
    print(host, port, password, database_name, user, password)
    if host is None or port is None or database_name is None or user is None or password is None:
        raise Exception('Database connection error')
    return "postgresql://"+user+":"+password+"@"+host+":"+port+"/"+database_name
