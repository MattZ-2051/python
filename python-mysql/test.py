import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="test_schema",
    auth_plugin='mysql_native_password'
)

mycursor = db.cursor()

# mycursor.execute(
# "CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")

mycursor.execute(
    "INSERT INTO PERSON (name, age) VALUES (%s,%s)", ('matt', 22))
db.commit()
