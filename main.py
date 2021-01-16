import database

class Bookcase:
    """ 
    Main class based on Singleton design pattern. 
    """
    __instance__ = None
    c = None
    conn = None

    def __init__(self):
        # Constructor.
        if Bookcase.__instance__ is None:
            Bookcase.__instance__ = self
            Bookcase.c, Bookcase.conn = database.start_connection()
        else:
            raise Exception("You cannot create another Bookcase class")

    @staticmethod
    def get_instance():
        # Static method to fetch the current instance.
        if not Bookcase.__instance__:
            Bookcase()
        return Bookcase.__instance__



""" 
TESTS

"""
Bookcase()

# TODO:
# nazwy
