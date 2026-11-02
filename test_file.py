import faker
from pymysql.cursors import Cursor

from lib.db import create_customer, delete_customer, get_columns_by_id, update_customer


def test_create_user(cursor: Cursor) -> None:
    fake = faker.Faker()
    firstname = fake.first_name()
    lastname = fake.last_name()
    user_data = {
    "id_gender": 1,
    "firstname": firstname,
    "lastname": lastname,
    "email": fake.email(),
    "passwd": fake.password(),
    "birthday": fake.date_of_birth(),
    "date_add": fake.date(),
    "date_upd": fake.date()
    }
    new_id = create_customer(cursor, user_data)
    result = get_columns_by_id(cursor, "ps_customer", "id_customer", new_id)
    assert result is not None
    assert result["id_customer"] == new_id, f"Пользователь с {new_id} не создался"
    assert result["firstname"] == firstname, f"Пользователь с {new_id} не создался"
    assert result["lastname"] == lastname, f"Пользователь с {new_id} не создался"


def test_update_customer(cursor: Cursor) -> None:
    fake = faker.Faker()
    firstname = fake.first_name()
    lastname = fake.last_name()
    email = fake.email()
    number_update = update_customer(cursor, 1, firstname, lastname, email)
    assert number_update == 1, "Нет пользователя для обновления"
    result = get_columns_by_id(cursor, "ps_customer", "id_customer", 1)
    assert result is not None, "Пользователь с id_customer = 1  нет"
    assert result["id_customer"] == 1, "Пользователь с id_customer = 1  нет"
    assert result["firstname"] == firstname, "Не обновилось имя у пользователя"
    assert result["lastname"] == lastname, "Не обновилось фамилия у пользователя"
    assert result["email"] == email, "Не обновился email у пользователя"

def test_update_customer_with_incorrect_date(cursor: Cursor) -> None:
    number_update = update_customer(cursor, 100, "TEST", "TES", "test@test.ru")
    assert number_update == 0, "Есть пользователь с id_customer = 100"
    result = get_columns_by_id(cursor, "ps_customer", "id_customer", 100)
    assert result is None, "Есть пользователь с id_customer = 100"

def test_delete_customer(cursor: Cursor) -> None:
    number_delete = delete_customer(cursor, 1)
    assert number_delete == 1, "Пользователь с id_customer = 1  нет"
    result = get_columns_by_id(cursor, "ps_customer", "id_customer", 1)
    assert result is None, "Пользователь с id_customer = 1  не удалился"

def test_delete_customer_with_incorrect_date(cursor):
    number_delete = delete_customer(cursor, 100)
    assert number_delete == 0, "Есть пользователь с id_customer = 100"
    result = get_columns_by_id(cursor, "ps_customer", "id_customer", 100)
    assert result is None, "Есть пользователь с id_customer = 100"