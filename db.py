import sqlite3
from rem import reminder


def db_saver(user_id: str, message: str, store: str) -> None:
    """
    :param user_id: user_info table param
    :param message: user_info table param (game URL)
    :param store: user_info table param
    :return: None

    Create DB connection, create table if not exists,
    insert get parameters into table.
    """
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
    """
    :param user_id: user_id used for selecting all users rows
    :return: list which contains URLs, price, actual_price, store

    Selecting all user's data from DB.
    """
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT message, price, actual_price, store FROM user_info WHERE user_id={user_id}')
        return [(i[0], i[1], i[2], i[3]) for i in cursor.fetchall()]
    except sqlite3.OperationalError:
        return []


def user_urls_extract(user_id: str) -> list:
    """
    :param user_id: user_id used for selecting all users URLs
    :return: list of user's URLs

    Returns list of user's URLs.
    """
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT message FROM user_info WHERE user_id={user_id}')
        return [(i[0]) for i in cursor.fetchall()]
    except sqlite3.OperationalError:
        return []


def db_delete(message: str, user_id: str) -> None:
    """
    :param message: User's URL
    :param user_id: User's id
    :return: None

    Delete specific game from DB.
    """
    conn = sqlite3.connect('user_info.db')
    sql = f'DELETE FROM user_info WHERE message=? AND user_id=?'
    cursor = conn.cursor()
    cursor.execute(sql, (message, user_id))
    conn.commit()


def price_set(message: str, user_id: str) -> None:
    """
    :param message: User's URL
    :param user_id: User's id
    :return: None

    Set specific game price(0 by default) to users desired price.
    """
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f'UPDATE user_info SET price="{message}"'
                   f'WHERE user_id={user_id} AND id=(SELECT max(id) FROM user_info)')
    conn.commit()


def new_price(price: int, link: str) -> None:
    """
    :param price: Scrapped price
    :param link: Game URL
    :return: None

    Update actual price for specific link, compare desired price and actual price,
    call reminder if actual price is lower than desired price.
    """
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT user_id, price, message, actual_price FROM user_info WHERE message="{link}"')
    id_and_desired_price = [(i[0], i[1], i[2]) for i in cursor.fetchall()]
    desired_price = id_and_desired_price[0][1]
    user_id = id_and_desired_price[0][0]
    link = id_and_desired_price[0][2]
    if int(desired_price) > price:
        reminder(user_id, link, price, desired_price)
    cursor.execute(f'UPDATE user_info SET actual_price={price} WHERE message="{link}"')
    conn.commit()


def store_urls_extract(store: str) -> list:
    """
    :param store: Store row in DB
    :return: Unique list of specific store URLs

    Returns all specific store URLs.
    """
    conn = sqlite3.connect('user_info.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT message FROM user_info WHERE store="{store}"')
    urls = set([i[0] for i in cursor.fetchall()])
    return list(urls)
