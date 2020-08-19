import pyodbc

import os

#absfilepath=os.path.abspath(os.getcwd()+'/')

#print(absfilepath)

connstr=('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
'DBQ={potato_db.accdb};')

print(connstr)

conn = pyodbc.connect(connstr, autocommit=True)
