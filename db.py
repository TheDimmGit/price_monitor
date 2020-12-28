import sqlite3


def db_saver(user_id: str, message: str) -> None:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_info
                    (id INTEGER PRIMARY KEY,
                      user_id integer,
                      message text)
                    """)
    cursor.execute(f"INSERT INTO user_info(user_id, message) VALUES (?,?)", (user_id, message))
    conn.commit()


def db_extract(user_id: str) -> list:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT message FROM user_info WHERE user_id={user_id}')
    game = set([i[0] for i in cursor.fetchall()])
    return list(game)


def db_delete(message: str) -> None:
    conn = sqlite3.connect('user_info.db')
    sql = 'DELETE FROM user_info WHERE message=?'
    cursor = conn.cursor()
    cursor.execute(sql, (message,))
    conn.commit()
