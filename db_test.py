from db import PerevalDB

db = PerevalDB()

# пользователь
user_id = db.add_user(
    email="test@mail.ru",
    fam="Иванов",
    name="Иван",
    otc="Иванович",
    phone="+7 900 000 00 00"
)

print("USER ID:", user_id)

# координаты
coord_id = db.add_coords(
    latitude=45.3842,
    longitude=7.1525,
    height=1200
)

print("COORD ID:", coord_id)

# перевал
pereval_id = db.add_pereval(
    beauty_title="пер.",
    title="Тестовый перевал",
    other_titles="Тест",
    connect="",
    user_id=user_id,
    coord_id=coord_id,
    level_winter="",
    level_summer="1А",
    level_autumn="1А",
    level_spring=""
)

print("PEREVAL ID:", pereval_id)

# изображение
db.add_image(
    pereval_id=pereval_id,
    image_data=b"test image bytes",
    title="Тестовое фото"
)

print("IMAGE ADDED")