import sqlite3
import config

conn = sqlite3.connect(config.DATABASE, check_same_thread=False)
cursor = conn.cursor()


def get_users_ids():
    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()
    return users

def add_new_order(date, time, type_photo, phone, city, user_id):
    cursor.execute(
        "INSERT INTO orders (date, time, type, place, number_phone, user_id) VALUES (?, ?, ?, ?, ?, ?)",
        (date, time, type_photo, city, phone, user_id)
    )
    conn.commit()

def get_password(user_id):
    cursor.execute('SELECT password FROM users WHERE user_id = ?',(user_id,))
    password = cursor.fetchall()
    if password is None or password[0][0] == '':
        config.logging.info(f'[{user_id}] У користувача немає записів у базі або пароль не порожній')
        return None
    else:
        return password[0][0], user_id

def add_password(user_id, password):
    cursor.execute(
        'UPDATE users SET password = ? WHERE user_id = ?',
        (password, user_id)
    )
    conn.commit()


def get_user_orders(user_id):
    cursor.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,))
    orders = cursor.fetchall()
    if not orders:
        config.logging.info(f'[{user_id}] У користувача немає записів до дб')
        return None
    else:
        return orders

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    users = [u[0] for u in get_users_ids()]

    if user_id in users:
        config.logging.info(f'[{user_id}] Користувач вже має запис до дб')
        return

    cursor.execute(
        'INSERT INTO users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)',
         (user_id, user_name, user_surname, username)
    )
    conn.commit()

    config.logging.info(f'[{user_id}] Додано користувача до дб')

def db_table_orders(user_id: int):
    orders = get_user_orders(user_id)
    if not orders:
        return None

    return orders

def get_order_by_id(order_id):
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    return order

def update_order(order_id, date, time, type_, place, phone):
    cursor.execute("""
        UPDATE orders
        SET date=?, time=?, type=?, city=?, phone=?
        WHERE id=?
    """, (date, time, type_, place, phone, order_id))
    conn.commit()

def delete_order_by_id(order_id):
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
