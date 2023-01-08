import MySQLdb

mysql_host = "localhost"
username = "root"
password = "root123##"

db = MySQLdb.connect(mysql_host, username, password)
cursor = db.cursor()
cursor.execute("CREATE DATABASE if not exists malware_urls;")
cursor.execute("USE malware_urls;")
query = "CREATE TABLE if not exists malware_url_info (url VARCHAR(512) PRIMARY KEY);"
cursor.execute(query)
