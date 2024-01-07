import sqlite3
import uuid

connection = sqlite3.connect("./knitten.db")


def get_all_products(connection=connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM products")
        raw_records = result.fetchall()
        records = [
            {
                "id": raw_record[0],
                "name": raw_record[1],
                "description": raw_record[2],
                "patterns": raw_record[3],
                "image_url": raw_record[4],
            }
            for raw_record in raw_records
        ]
        return records


def delete_product(id_: str, connection=connection):
    with connection:
        connection.execute("DELETE FROM products WHERE id = ?", (id_,))


def update_product(product_record: dict, connection=connection):
    with connection:
        connection.execute(
            """UPDATE products SET
                name = ?,
                description = ?,
                patterns = ?,
                image_url = ?
            WHERE id = ?
            """,
            (
                product_record["name"],
                product_record["description"],
                product_record["patterns"],
                product_record["image_url"],
                product_record["id"],
            )
        )


def insert_product(product_record: dict, connection=connection):
    with connection:
        connection.execute(
            """INSERT INTO products VALUES (?, ?, ?, ?, ?)""",
            (
                product_record["id"],
                product_record["name"],
                product_record["description"],
                product_record["patterns"],
                product_record["image_url"],
            )
        )


def get_all_users(connection=connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("SELECT id, role, username, full_name, password FROM users")
        raw_records = result.fetchall()
        records = [
            {
                "id": raw_record[0],
                "role": raw_record[1],
                "username": raw_record[2],
                "full_name": raw_record[3],
                "password": raw_record[4],
            }
            for raw_record in raw_records
        ]
        return records


def get_all_yarns(connection=connection):
    with connection:
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM yarns")
        raw_records = result.fetchall()
        records = [
            {
                "id": raw_record[0],
                "name": raw_record[1],
                "color": raw_record[2],
                "price_per_unit": raw_record[3],
            }
            for raw_record in raw_records
        ]
        return records


def insert_yarn(yarn_record: dict, connection=connection):
    with connection:
        connection.execute(
            """INSERT INTO yarns VALUES (?, ?, ?, ?)""",
            (
                yarn_record["id"],
                yarn_record["name"],
                yarn_record["color"],
                yarn_record["price_per_unit"],
            )
        )


def update_yarn(yarn_record: dict, connection=connection):
    with connection:
        connection.execute(
            """UPDATE yarns SET
                name = ?,
                color = ?,
                price_per_unit = ?
            WHERE id = ?
            """,
            (
                yarn_record["name"],
                yarn_record["color"],
                yarn_record["price_per_unit"],
                yarn_record["id"],
            )
        )


def delete_yarn(id_: str, connection=connection):
    with connection:
        connection.execute("DELETE FROM yarns WHERE id = ?", (id_,))


def get_product_yarns(product_id: str):
    with connection:
        raw_records = connection.execute(
            """
            SELECT y.*, py.yarn_count, py.product_id, py.id FROM yarns y
            JOIN product__yarn py
            ON py.yarn_id = y.id
            AND py.product_id = ?
            """,
            (product_id,)
        ).fetchall()
        records = [
            {
                "yarn_id": raw_record[0],
                "yarn_name": raw_record[1],
                "yarn_color": raw_record[2],
                "yarn_price_per_unit": raw_record[3],
                "yarn_count": raw_record[4],
                "product_id": raw_record[5],
                "id": raw_record[6],
            }
            for raw_record in raw_records
        ]
        return records


def update_product_yarn(record: dict, connection=connection):
    with connection:
        connection.execute(
            """
            UPDATE product__yarn
            SET yarn_count = ?,
                product_id = ?,
                yarn_id = ?
            WHERE id = ?
            """,
            (
                record["yarn_count"],
                record["product_id"],
                record["yarn_id"],
                record["id"],
            )
        )


def insert_product_yarn(record: dict, connection=connection):
    with connection:
        connection.execute(
            """INSERT INTO product__yarn VALUES (?, ?, ?, ?)""",
            (
                record["id"],
                record["product_id"],
                record["yarn_id"],
                record["yarn_count"],
            )
        )


def delete_product_yarn(id_: str, connection=connection):
    with connection:
        connection.execute("DELETE FROM product__yarn WHERE id = ?", (id_,))


def insert_user(user_record: dict, connection=connection):
    with connection:
        connection.execute(
            "INSERT INTO users (id, role, username, full_name, email, password) VALUES (?, ?, ?, ?, ?, ?)",
            (
                user_record["id"],
                user_record["role"],
                user_record["username"],
                user_record["full_name"],
                user_record["email"],
                user_record["password"],
            )
        )


def insert_order(cart: dict, user_id: str, user_message: str, state: str):
    with connection:
        order_id = str(uuid.uuid4())
        connection.execute(
            "INSERT INTO orders (id, user_id, user_message, state) VALUES (?, ?, ?, ?)",
            (
                order_id,
                user_id,
                user_message,
                state,
            ),
        )
        for product_id, product_count in cart.items():
            connection.execute(
                "INSERT INTO order_products (id, order_id, product_id, product_count) VALUES (?, ?, ?, ?)",
                (
                    str(uuid.uuid4()),
                    order_id,
                    product_id,
                    product_count,
                )
            )


def get_user(id_: str):
    with connection:
        raw_user = connection.execute(
            "SELECT id, role, username, email, full_name, password FROM users WHERE id = ?",
            (id_,)
        ).fetchone()
        user = {
            "id": raw_user[0],
            "role": raw_user[1],
            "username": raw_user[2],
            "email": raw_user[3],
            "full_name": raw_user[4],
            "password": raw_user[5],
        }
        return user


def get_product_price(id_: str):
    price = 0
    with connection:
        product_yarns = get_product_yarns(product_id=id_)
        for product_yarn in product_yarns:
            price += product_yarn["yarn_price_per_unit"] * product_yarn["yarn_count"]

    return price


def get_orders():
    with connection:
        raw_orders = connection.execute(
            "SELECT id, user_id, user_message, state, date_created FROM orders"
        ).fetchall()
        orders = [
            {
                "id": raw_order[0],
                "user_id": raw_order[1],
                "user_message": raw_order[2],
                "state": raw_order[3],
                "date_created": raw_order[4],
            }
            for raw_order in raw_orders
        ]

        for order in orders:
            user_id = order["user_id"]
            user = get_user(id_=user_id)
            order["user"] = user

        raw_order_products = connection.execute(
            """
            SELECT p.id, name, description, patterns, image_url, order_id, product_count
            FROM products p
            JOIN order_products op
            ON p.id = op.product_id
            """,
        )
        order_product_records = [
            {
                "product_id": raw_order_product[0],
                "product_name": raw_order_product[1],
                "product_description": raw_order_product[2],
                "product_patterns": raw_order_product[3],
                "product_image_url": raw_order_product[4],
                "order_id": raw_order_product[5],
                "product_count": raw_order_product[6],
            }
            for raw_order_product in raw_order_products
        ]
        for order_product_record in order_product_records:
            order_product_record["product_price"] = get_product_price(id_=order_product_record["product_id"])

        orders_products = {}
        for order_product_record in order_product_records:
            order_id = order_product_record["order_id"]
            if order_id not in orders_products:
                orders_products[order_id] = [order_product_record]
            else:
                orders_products[order_id].append(order_product_record)

        for order in orders:
            order_id = order["id"]
            if order_id not in orders_products:
                order["products"] = []
            else:
                order["products"] = orders_products[order_id]

        for order in orders:
            order_price = 0
            for order_product in order["products"]:
                order_price += order_product["product_price"] * order_product["product_count"]
            order["price"] = order_price

        return orders


def delete_order(id_: str):
    with connection:
        connection.execute("DELETE FROM orders WHERE id = ?", (id_,))


def update_order(order: dict):
    with connection:
        connection.execute(
            """
            UPDATE orders SET
                state = ?
            WHERE id = ?
            """,
            (
                order["state"],
                order["id"],
            )
        )
