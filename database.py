import sqlite3

def start_connection():
    conn = sqlite3.connect('example.db')
    return conn.cursor(), conn

def close_connection(conn):
    conn.close()

def add_book_toDB(c, conn, ID, title, author, category, rating, isRent, rentedPerson, dateCompleted, pageCount):
    c.execute("INSERT INTO bookcase VALUES ('%s', '%s', '%s', '%s', '%d', '%r', '%s', '%s', '%d')" % \
        (ID, title, author, category, rating, isRent, rentedPerson, dateCompleted, pageCount))
    conn.commit()

def get_books_fromDB(c):
    c.execute('SELECT * FROM bookcase')
    return c.fetchall()

def del_book_fromDB(c, conn, ID):
    c.execute('DELETE FROM bookcase where ID = %d' % ID)
    conn.commit()

def edit_book_inDB(c, conn, ID, param, new_val):
    c.execute("UPDATE bookcase SET %s = '%s' where ID = %d" % param, new_val, ID)
    conn.commit()

def sort_books(books, param, rev):
    return [tpl for tpl in sorted(books, key=lambda item: item[param], reverse=rev)]

def filter_books(books, param, value):
    return [tpl for tpl in books if tpl[param]=value]

c, conn = start_connection()
print(get_books_fromDB(c))
print(sort_books(get_books_fromDB(c), 7, True))