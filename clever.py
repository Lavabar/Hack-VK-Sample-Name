import pymysql

def start(nam, phon):
    conn = pymysql.connect(host='185.117.152.219', user='hack', password='Wzfuv175', database='hack')
    cursor = conn.cursor()
    #data = (str(None), str(nam), str(phon))
    cursor.execute("insert into users1 (nam, phone) values ('test', '123');")
    #cursor.execute("""insert into users1 (id, name, phone) values (NULL, {0}, {1}""".format(str("\'" + nam + "\'" ), str("\'" + phon + "\'" )))
    print(cursor.execute("select * from users1"))
    conn.close()
    print(nam)
    print(phon)
    return "true"
