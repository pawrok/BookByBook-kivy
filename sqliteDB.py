import sqlite3

class SqliteDB:
    " Singleton class "
    __instance__ = None
    c = None # cursor
    conn = None # connection

    def __init__(self):
        # Constructor.
        if SqliteDB.__instance__ is None:
            SqliteDB.__instance__ = self
            SqliteDB.c, SqliteDB.conn = SqliteDB.start_connection()
        else:
            raise Exception("You cannot create another SqliteDB class")

    @staticmethod
    def get_instance():
        # Static method to fetch the current instance.
        if not SqliteDB.__instance__:
            SqliteDB()
        return SqliteDB.__instance__

    def start_connection():
        conn = sqlite3.connect('example.db')
        conn.row_factory = sqlite3.Row
        return conn.cursor(), conn

    def close_connection():
        SqliteDB.conn.close()

    def create_table(table_name = "booktable"):
        SqliteDB.c.execute('''CREATE TABLE if not exists %s
        (
            ID INTEGER,
            title TEXT,
            author TEXT,
            category TEXT,
            rating INTEGER,
            isRent INTEGER,
            rentedPerson TEXT,
            dateCompleted TEXT,
            pageCount INTEGER
        )''' % table_name)

    def add_book_toDB(
            ID, title, author, category = '', rating = 0, \
            isRent = 0, rentedPerson = '', dateCompleted = '', \
            pageCount = 0):
        SqliteDB.c.execute("INSERT INTO booktable VALUES ('%s', '%s', '%s', '%s', '%d', '%r', '%s', '%s', '%d')" % \
            (ID, title, author, category, rating, isRent, rentedPerson, dateCompleted, pageCount))
        SqliteDB.conn.commit()

    def get_books_fromDB():
        SqliteDB.c.execute('SELECT * FROM booktable')
        # result = 
        return [dict(row) for row in SqliteDB.c.fetchall()]

    def del_book_fromDB(ID):
        SqliteDB.c.execute('DELETE FROM booktable where ID = %d' % ID)
        SqliteDB.conn.commit()

    def edit_book_inDB(ID, param, new_val):
        SqliteDB.c.execute("UPDATE booktable SET %s = '%s' where ID = %d" % param, new_val, ID)
        SqliteDB.conn.commit()

    def sort_books(books, param, rev):
        return [tpl for tpl in sorted(books, key=lambda item: item[param], reverse=rev)]

    def filter_books(books, param, value):
        return [tpl for tpl in books if tpl[param] == value]

# SqliteDB()
# SqliteDB.create_table()
# SqliteDB.add_book_toDB(1, 'title1', 'author1')
# SqliteDB.del_book_fromDB(1)
# print(SqliteDB.get_books_fromDB())
# print(sort_books(get_books_fromDB(c), 7, True))