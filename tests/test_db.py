from db import PerevalDB


def test_add_and_get_user():
    db = PerevalDB()

    user_id = db.add_user(
        email="test@test.ru",
        fam="Тестов",
        name="Тест",
        otc="Тестович",
        phone="+70000000000"
    )

    assert user_id is not None