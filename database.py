import sqlite3

db = sqlite3.connect("zilsistemi/zilsistemi.db")
connection = db.cursor()

# aşağıda """ olarak da yapabilirdik, bütün ifadeyi stringe alıyor
create_user_table_query = "create table if not exists user(\
    id integer primary key autoincrement,\
    username text not null unique, \
    password text not null)"
    # sicil no id no olabilir, uniq değer
    # şifre belirlenirken büyük küçük sayı kullanımı uyarısı at
connection.execute(create_user_table_query)
db.commit()
db.close()
