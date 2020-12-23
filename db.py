import sqlite3


def db_saver(user_id, message):
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_info
                    (id INTEGER PRIMARY KEY,
                      user_id integer,
                      message text)
                    """)
    info = list(tuple(user_id, message))
    cursor.execute(f"INSERT INTO user_info(user_id, message) VALUES (?,?)", info)
    conn.commit()
