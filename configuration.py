import os.path


def get_db_path():
    dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(dir, 'sql')
    return db_path
