import os
import psycopg2
from psycopg2.extras import RealDictCursor

class PerevalDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("FSTR_DB_HOST"),
            port=os.getenv("FSTR_DB_PORT"),
            user=os.getenv("FSTR_DB_LOGIN"),
            password=os.getenv("FSTR_DB_PASS"),
            dbname=os.getenv("FSTR_DB_NAME"),
            cursor_factory=RealDictCursor
        )
        self.conn.autocommit = True

    def add_user(self, email, fam, name, otc, phone):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )
            user = cur.fetchone()
            if user:
                return user["id"]

            cur.execute(
                """
                INSERT INTO users (email, fam, name, otc, phone)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (email, fam, name, otc, phone)
            )
            return cur.fetchone()["id"]

    def add_coords(self, latitude, longitude, height):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO coords (latitude, longitude, height)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (latitude, longitude, height)
            )
            return cur.fetchone()["id"]

    def add_pereval(
            self,
            beauty_title,
            title,
            other_titles,
            connect,
            user_id,
            coord_id,
            level_winter,
            level_summer,
            level_autumn,
            level_spring
    ):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO pereval_added (
                    beauty_title,
                    title,
                    other_titles,
                    connect,
                    user_id,
                    coord_id,
                    level_winter,
                    level_summer,
                    level_autumn,
                    level_spring,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'new')
                RETURNING id
                """,
                (
                    beauty_title,
                    title,
                    other_titles,
                    connect,
                    user_id,
                    coord_id,
                    level_winter,
                    level_summer,
                    level_autumn,
                    level_spring
                )
            )
            return cur.fetchone()["id"]

    def add_image(self, pereval_id, image_data, title):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO pereval_images (pereval_id, image_data, title)
                VALUES (%s, %s, %s)
                """,
                (pereval_id, image_data, title)
            )
