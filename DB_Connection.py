import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-VJICLGS\MYSQLSERVER;'
                          'Database=SDMFinalAssignment;'
                          'Trusted_Connection=yes;')

def insert(tweet, image_url, sentiment):
    cursor = conn.cursor()
    query = "Insert into SDMFinalAssignment.dbo.tweets (text, image_url, sentiment) values ('%s','%s','%s')" % (tweet, image_url,sentiment)
    cursor.execute(query)
    conn.commit()

def select():
    cursor = conn.cursor()
    print(cursor)
    cursor.execute('SELECT * FROM SDMFinalAssignment.dbo.tweets')
    myresult = cursor.fetchall()
    conn.commit()
    return myresult