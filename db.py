import sqlite3


def db_saver(user_id: str, message: str) -> None:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_info
                    (id INTEGER PRIMARY KEY,
                    user_id integer,
                    message text,
                    price text NOT NULL DEFAULT 0,
                    actual_price text NOT NULL DEFAULT 0)
                    """)
    conn.commit()
    cursor.execute(f"INSERT INTO user_info(user_id, message, price, actual_price) "
                   f"VALUES (?,?,?,?)", (user_id, message, '0', '0'))
    conn.commit()


def db_extract(user_id: str) -> list:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM user_info WHERE user_id={user_id}')
        return [(i[2], i[3]) for i in cursor.fetchall()]
    except sqlite3.OperationalError:
        return []


def db_delete(message: str) -> None:
    conn = sqlite3.connect('user_info.db')
    sql = 'DELETE FROM user_info WHERE message=?'
    cursor = conn.cursor()
    cursor.execute(sql, (message,))
    conn.commit()


def price_update(message: str, user_id: str) -> None:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE user_info SET price={message} '
                   f'WHERE user_id={user_id} AND id=(SELECT max(id) FROM user_info)')
    conn.commit()


def new_price(price, link):
    conn = sqlite3.connect('../../user_info.db')
    cursor = conn.cursor()
    print(f'UPDATE user_info SET actual_price={price} WHERE message={link}')
    cursor.execute(f'UPDATE user_info SET actual_price={price} WHERE message="{link}"')
    conn.commit()


def urls_extract():
    conn = sqlite3.connect('../../user_info.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM user_info')
    urls = set([i[0] for i in cursor.fetchall()])
    return list(urls)


