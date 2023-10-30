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
