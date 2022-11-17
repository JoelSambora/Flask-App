import mysql.connector as mysql
from mysql.connector import Error

try:
    connection = mysql.connect(host='localhost',
                                database='teste',
                                user='root',
                                password='')
    
    cursor = connection.cursor(buffered=True)
    
    mySql_Create_Table_Query = """CREATE TABLE date_time ( 
                            Id int AUTO_INCREMENT PRIMARY KEY,
                            d_date varchar(250) NOT NULL UNIQUE,
                            t_time BOOLEAN NOT NULL, 
                            FOREIGN KEY(Colaboradores_ID) REFERENCES Colaboradores(Id)
                            ) """
    
    cursor = connection.cursor(buffered=True)
    result = cursor.execute(mySql_Create_Table_Query)
    print("Users Table created successfully ")
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")       