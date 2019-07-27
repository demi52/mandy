import os

try:
    import cx_Oracle
except:
    os.system("pip install cx_Oracle-7.0.0.tar.gz")

try:
    import HTMLReport
except:
    os.system("pip install HTMLReport-1.5.1.tar.gz")

try:
    import pymysql
except:
    os.system("pip install PyMySQL-0.9.3.tar.gz")

try:
    import requests
except:
    os.system("pip install requests-2.21.0.tar.gz")

try:
    import selenium
except:
    os.system("pip install selenium-3.141.0.tar.gz")

try:
    import xlrd
except:
    os.system("pip install xlrd-1.2.0.tar.gz")

try:
    import xlwt
except:
    os.system("pip install xlwt-1.3.0.tar.gz")

try:
    import django
except:
    os.system("pip install Django-2.2.tar.gz")