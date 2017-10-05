import MySQLdb
db = MySQLdb.connect("rsingh.mysql.pythonanywhere-services.com","rsingh","golusingh","rsingh$testDb" )
cursor = db.cursor()
cursor.execute("select count(*) from user where emailId LIKE "+"'abc@gmail.com'")
data = cursor.fetchone()
print "Database version : %s ",data[0]
db.close()
