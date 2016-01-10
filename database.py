import os
import logging
import sqlite3
import configuration

db_path = configuration.get_db_path()
os.makedirs(db_path, exist_ok=True)
sfile = db_path + '/db.sqlite'

logger = logging.getLogger(__name__)


def init_table():
    conn = sqlite3.connect(sfile)
    cur = conn.cursor()
    cur.execute('''create table if not exists
    reminders(
        id integer primary key,
        name text,
        description text,
        date_time text
    )
    ''')
    conn.commit()
    conn.close()


def get_reminders():
    conn = sqlite3.connect(sfile)
    cur = conn.cursor()
    reminders = cur.execute('''select id, name, description, date_time
    from reminders''').fetchall()
    conn.close()
    return reminders


def add_reminder(name, description, date_time):
    '''Inserts a new reminder row.
    Args:
        name: A reminder's title.
        description: A reminder's desccd ription.
        date_time: Date and time in YYYY-MM-DD HH:MM:SS format.
    Returns:
        Index of the inserted row.
    '''

    conn = sqlite3.connect(sfile)
    cur = conn.cursor()
    cur.execute('''insert into reminders(name, description, date_time)
    values(?,?,?)''', (name, description, date_time))
    conn.commit()
    conn.close()
    logger.info('A new reminder was saved')
    return cur.lastrowid


def remove_reminder(r_id):
    conn = sqlite3.connect(sfile)
    cur = conn.cursor()
    cur.execute("delete from reminders where id=?", (r_id,))
    conn.commit()
    conn.close()
    logger.info('A reminder with id %d was removed', r_id)

init_table()
