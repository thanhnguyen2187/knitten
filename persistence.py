import sqlite3

connection = sqlite3.connect("./knitten.db")


def get_all_products(connection=connection):
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
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM users")
    raw_records = result.fetchall()
    records = [
        {
            "id": raw_record[0],
            "username": raw_record[1],
            "full_name": raw_record[2],
            "password": raw_record[3],
        }
        for raw_record in raw_records
    ]
    return records


def get_all_yarns(connection=connection):
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

