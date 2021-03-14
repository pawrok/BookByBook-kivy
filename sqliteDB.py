import sqlite3

class SqliteDB:
    " Singleton class "
    __instance__ = None
    c = None        # cursor
    conn = None     # connection

    def __init__(self):
        # Constructor
        if SqliteDB.__instance__ is None:
            SqliteDB.__instance__ = self
            SqliteDB.c, SqliteDB.conn = SqliteDB.start_connection()
            SqliteDB.create_book_table()
            SqliteDB.create_extra_tables()
        else:
            raise Exception("You cannot create another SqliteDB class")

    @staticmethod
    def get_instance():
        # Static method to fetch the current instance
        if not SqliteDB.__instance__:
            SqliteDB()
        return SqliteDB.__instance__

    def start_connection():
        conn = sqlite3.connect('books.db')
        conn.row_factory = sqlite3.Row
        return conn.cursor(), conn

    def close_connection():
        SqliteDB.conn.close()

    # --------------- Books DB ------------------

    def create_book_table():
        SqliteDB.c.execute('''CREATE TABLE if not exists booktable
        (
            book_id INTEGER,
            title TEXT,
            author TEXT,
            category TEXT,
            rating INTEGER,
            rentedPerson TEXT,
            dateCompleted TEXT,
            pageCount INTEGER,
            isRead INTEGER,
            imageDest TEXT,
            isFav INTEGER,
            describtion TEXT,
            shelves TEXT,
            tags TEXT
        )''')

    def add_book_to_db(
            title, author, category, rating, rentedPerson,dateCompleted, 
            pageCount, isRead, imageDest, isFav, describtion, shelves, tags):
        
        # set book_id to max(book_id) + 1; fetchone() sometimes haven't worked
        SqliteDB.c.execute("SELECT MAX(book_id) FROM booktable")
        max_dict = [dict(row) for row in SqliteDB.c.fetchall()]
        
        try:
            max_id = max_dict[0]['MAX(book_id)'] + 1
        except:
            max_id = 1
        
        shelves = ';'.join(shelves)
        tags = ';'.join(tags)

        SqliteDB.c.execute(
            f"""INSERT INTO booktable VALUES (
                '{max_id}', '{title}', '{author}', '{category}', '{rating}',
                '{rentedPerson}', '{dateCompleted}', '{pageCount}',
                '{isRead}', '{imageDest}', '{isFav}', '{describtion}',
                '{shelves}', '{tags}')""")
        
        SqliteDB.conn.commit()

    def get_single_book_from_db(book_id):
        SqliteDB.c.execute(f'SELECT * FROM booktable WHERE book_id = {book_id}')
        selected_book = SqliteDB.c.fetchone()
        
        if selected_book != None:
            return dict(selected_book)
        else:
            return 0

    def del_book_from_db(book_id):
        SqliteDB.c.execute(f'DELETE FROM booktable where book_id = {book_id}')
        SqliteDB.conn.commit()

    def edit_book_in_db(
            book_id, title, author, category, rating, rentedPerson, 
            dateCompleted, pageCount, isRead, imageDest, isFav, describtion, 
            shelves, tags):
        shelves = ';'.join(shelves)
        tags = ';'.join(tags)
        
        sql = """
            UPDATE booktable SET 
                title = ?,
                author = ?,
                category = ?,
                rating = ?,
                rentedPerson = ?,
                dateCompleted = ?,
                pageCount = ?,
                isRead  = ?,
                imageDest  = ?,
                isFav  = ?,
                describtion  = ?,
                shelves = ?,
                tags = ?
            WHERE 
                book_id = ?
            """
        
        SqliteDB.c.execute(sql, (title, author, category, rating, rentedPerson,
                                dateCompleted, pageCount, isRead, imageDest,
                                isFav, describtion, shelves, tags, book_id))
        SqliteDB.conn.commit()

    def sort_books(books, param, rev):
        return [tpl for tpl in sorted(books, key=lambda item: item[param],
                                      reverse=rev)]

    def filter_books(books, param, value):
        return [tpl for tpl in books if tpl[param] == value]
    
    def get_db_values(table_name):
        SqliteDB.c.execute(f'SELECT * FROM {table_name}')
        return [dict(row) for row in SqliteDB.c.fetchall()]

    # ------------- Shelves and tags DB ------------------

    def create_extra_tables():
        SqliteDB.c.execute(
            '''CREATE TABLE IF NOT EXISTS shelves (shelf TEXT)''')
        
        SqliteDB.c.execute(
            '''CREATE TABLE IF NOT EXISTS tags (tag TEXT)''')


    def insert_to(table, value):
        SqliteDB.c.execute(f"INSERT INTO {table} VALUES ('{value}')")
        SqliteDB.conn.commit()

    def del_value_from(table, value, row_type):
        SqliteDB.c.execute(f'DELETE FROM {table} WHERE {row_type} = \'{value}\'')
        SqliteDB.conn.commit()
