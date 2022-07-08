import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="test_schema",
    passwd="Pass@123",
    auth_plugin='mysql_native_password'
)

mycursor = db.cursor()

# Example of creating a Schema in MYSQL using python connector

# mycursor.execute(
# "CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")

# Example of creating new object in schema and committing it to DB

# mycursor.execute(
#     "INSERT INTO PERSON (name, age) VALUES (%s,%s)", ('matt', 22))
# db.commit()

# mycursor.execute(
# "CREATE TABLE Test (name varchar(50) NOT NULL, created datetime NOT NULL, gender ENUM('M', 'F', 'O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

# mycursor.execute("INSERT INTO TEST (name, created, gender) VALUES (%s, %s, %s)",
#                  ("JACK", datetime.now(), "O"))
# db.commit()
