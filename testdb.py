from db import db
with db('test_db') as mysql_db:
    # values: ((columns, value, type),...)
    values = (('id','2','int'),('value','2','int'))
    mysql_db.insert_db('test_table', values)
