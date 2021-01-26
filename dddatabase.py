import os
import psycopg2
from psycopg2 import ProgrammingError

insert_sql = '''
    INSERT INTO dd_character (user_id, str, dex, con, wis, int, cha) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET
    (str, dex, con, wis, int, cha) = (EXCLUDED.str, EXCLUDED.dex, EXCLUDED.con, EXCLUDED.wis, EXCLUDED.int, EXCLUDED.cha);
'''

fetch_sql = '''
    SELECT str, dex, con, wis, int, cha FROM dd_character WHERE user_id = %s
'''


def insert_character(user_id, content):

    conn = psycopg2.connect(
        host=os.getenv('PG_HOSTNAME'),
        database=os.getenv('PG_DATABASE'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'))

    for x in range(1, 6):
        if not content[x].isdigit():
            return 1

    cur = conn.cursor()
    cur.execute(insert_sql, (user_id, int(content[1]), int(content[2]), int(content[3]),
                             int(content[4]), int(content[5]), int(content[6])))

    conn.commit()

    cur.close()
    conn.close()

    return 0


def fetch_character(user_id):

    conn = psycopg2.connect(
        host=os.getenv('PG_HOSTNAME'),
        database=os.getenv('PG_DATABASE'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'))

    try:
        cur = conn.cursor()
        cur.execute(fetch_sql, (user_id,))

        stats = cur.fetchone()

        if stats is None:
            stats = [10, 10, 10, 10, 10, 10]

        cur.close()
        conn.close()
    except ProgrammingError:
        stats = [10, 10, 10, 10, 10, 10]

    return stats
