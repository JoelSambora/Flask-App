import pymysql
import mysql.connector
from mysql.connector import Error
pymysql.install_as_MySQLdb()
class Config:
    SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'

class DevelopmentConfig(Config):
    connection = mysql.connector.connect(host='localhost',
                                         database='teste',
                                         user='root',
                                         password='pynative@#29')



config = {
    'development': DevelopmentConfig
}