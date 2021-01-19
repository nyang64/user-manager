# database connection

def getConString():
    host = "es2db.caneampnjecs.us-west-1.rds.amazonaws.com"
    port = "5432"
    database = "escpdb"
    user = "dbadmin"
    password = "!Test12345"
    # host = "ziggy.db.elephantsql.com"
    # port = "5432"
    # database = "ghyvyxgx"
    # user = "ghyvyxgx"
    # password = "HDeVUah-zVES6mDqWPJCCuOTVUUNrEq_"
    return "postgresql://"+user+":"+password+"@"+host+":"+port+"/"+database
