
from typing import Any
from conftest import cursor
from pymysql.cursors import Cursor


def create_customer(cursor: Cursor, customer_data: dict) -> int:
    columns = ", ".join(customer_data.keys())
    placeholders = ", ".join([f"%({key})s" for key in customer_data.keys()])
    query = f"""INSERT INTO ps_customer ({columns}) VALUES ({placeholders})"""
    cursor.execute(query, customer_data)
    return cursor.lastrowid

def get_columns_by_id(cursor: Cursor, table: str, column_title: str, id_element: int) -> dict[str, Any] | tuple[Any, ...] | None:
    query = f"SELECT * FROM {table} WHERE {column_title} = %s"
    cursor.execute(query, (id_element, ))
    column = cursor.fetchone()
    return column

def update_customer(cursor, customer_id: int, firstname: str, lastname: str, email: str) -> int:
    query = """
            UPDATE ps_customer
            SET firstname = %s, lastname = %s, email = %s 
            WHERE id_customer = %s
        """
    cursor.execute(query, (firstname, lastname, email, customer_id))
    return cursor.rowcount

def delete_customer(cursor, customer_id: int) -> int:
    query = "DELETE FROM ps_customer WHERE id_customer = %s"
    cursor.execute(query, (customer_id, ))
    return cursor.rowcount