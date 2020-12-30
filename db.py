import sqlite3


def db_saver(user_id: str, message: str) -> None:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_info
                    (id INTEGER PRIMARY KEY,
                    user_id integer,
                    message text,
                    price text NOT NULL DEFAULT 0)
                    """)
    conn.commit()
    cursor.execute(f"INSERT INTO user_info(user_id, message, price) VALUES (?,?,?)", (user_id, message, '0'))
    conn.commit()


def db_extract(user_id: str) -> list:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM user_info WHERE user_id={user_id}')
        game = set([i for i in cursor.fetchall()])
        game_list = []
        for i in game:
            game_list.append(str(i[2])+'\n'+'Твоя желаемая цена - '+str(i[3]))
        return game_list
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
