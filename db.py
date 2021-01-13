import sqlite3
from reminder import reminder


def db_saver(user_id: str, message: str, store: str) -> None:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_info
                    (id INTEGER PRIMARY KEY,
                    user_id integer,
                    message text,
                    price text NOT NULL DEFAULT 0,
                    actual_price text NOT NULL DEFAULT 0,
                    store text)
                    """)
    conn.commit()
    cursor.execute(f"INSERT INTO user_info(user_id, message, price, actual_price, store) "
                   f"VALUES (?,?,?,?,?)", (user_id, message, '0', '0', store))
    conn.commit()


def db_extract(user_id: str) -> list:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT message, price, actual_price, store FROM user_info WHERE user_id={user_id}')
        return [(i[0], i[1], i[2], i[3]) for i in cursor.fetchall()]
    except sqlite3.OperationalError:
        return []


def link_extract(user_id: str) -> list:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT message FROM user_info WHERE user_id={user_id}')
        return [(i[0]) for i in cursor.fetchall()]
    except sqlite3.OperationalError:
        return []


def db_delete(message: str) -> None:
    conn = sqlite3.connect('user_info.db')
    sql = 'DELETE FROM user_info WHERE message=?'
    cursor = conn.cursor()
    cursor.execute(sql, (message,))
    conn.commit()


def price_set(message: str, user_id: str) -> None:
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE user_info SET price={message} '
                   f'WHERE user_id={user_id} AND id=(SELECT max(id) FROM user_info)')
    conn.commit()


def new_price(price, link):
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT user_id, price, message FROM user_info WHERE message='{link}'")
    id_and_desired_price = [(i[0], i[1], i[2]) for i in cursor.fetchall()]
    desired_price = id_and_desired_price[0][1]
    user_id = id_and_desired_price[0][0]
    link = id_and_desired_price[0][2]
    print(desired_price)
    print(user_id)
    print(link)
    if int(desired_price) >= price:
        reminder(user_id, link, price,desired_price)
    # TODO проверить желаемый прайс и если он равен или выше actual_price, то вызывать функцию, которая дудет принимать
    # TODO на воход айди пользователя, линк и актаульную цену
    print(f'UPDATE user_info SET actual_price={price} WHERE message={link}')
    cursor.execute(f'UPDATE user_info SET actual_price={price} WHERE message="{link}"')
    conn.commit()
    return desired_price, user_id, link


def urls_extract(store):
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT message FROM user_info WHERE store='{store}'")
    urls = set([i[0] for i in cursor.fetchall()])
    return list(urls)


def user_urls_extract(id):
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT message FROM user_info WHERE user_id={id}')
    urls = set([i[0] for i in cursor.fetchall()])
    return list(urls)

