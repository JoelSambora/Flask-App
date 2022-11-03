import mysql.connector as mysql
from mysql.connector import Error

try:
    connection = mysql.connect(host='localhost',
                                database='teste',
                                user='root',
                                password='')
    
    cursor = connection.cursor()
    
    mySql_Create_Table_Query = """CREATE TABLE Users ( 
                            Id int AUTO_INCREMENT PRIMARY KEY,
                            Email varchar(250) NOT NULL UNIQUE,
                            is_Admin BOOLEAN NOT NULL, 
                            Senha VARCHAR2(80) NOT NULL,
                            ) """
    
    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("Users Table created successfully ")                        

    mySql_Create_Table_Query = """CREATE TABLE Colaboradores(
                            Id int AUTO_INCREMENT PRIMARY KEY,
                            Users_id int(11) NOT NULL,
                            Nome varchar(250) NOT NULL,
                            Genero enum('Masculino', 'Feminino') NOT NULL,
                            FOREIGN KEY(Users_id) REFERENCES Users(Id)
                            )"""
    
    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("Colaboradores Table created successfully ")
    
    mySql_Create_Table_Query = """CREATE TABLE Endereco(
                            Id int AUTO_INCREMENT PRIMARY KEY,
                            Colaboradores_ID int(11) NOT NULL,
                            Provincia enum('Maputo Província', 'Maputo Cidade') NOT NULL,
                            Avenida varchar(250) NOT NULL,
                            Bairro varchar(250) NOT NULL,
                            Casa_Numero int (11) NOT NULL,
                            FOREIGN KEY(Colaboradores_ID) REFERENCES Colaboradores(Id)
                            )""" 
    
    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("Endereco Table created successfully ")
                            
    mySql_Create_Table_Query = """CREATE TABLE Telefone(
                            Id int AUTO_INCREMENT PRIMARY KEY,
                            Colaboradores_ID int(11) NOT NULL,
                            Telefone char(9) NOT NULL UNIQUE,
                            FOREIGN KEY(Colaboradores_ID) REFERENCES Colaboradores(Id)
                            )"""
                                                   
    cursor = connection.cursor()
    result = cursor.execute(mySql_Create_Table_Query)
    print("telefone Table created successfully ")
    
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")