import os
import base64
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

    def get_pereval_by_id(self, pereval_id: int):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    p.id,
                    p.beauty_title,
                    p.title,
                    p.other_titles,
                    p.connect,
                    p.add_time,
                    p.status,

                    u.email,
                    u.fam,
                    u.name,
                    u.otc,
                    u.phone,

                    c.latitude,
                    c.longitude,
                    c.height,

                    p.level_winter,
                    p.level_summer,
                    p.level_autumn,
                    p.level_spring
                FROM pereval_added p
                JOIN users u ON p.user_id = u.id
                JOIN coords c ON p.coord_id = c.id
                WHERE p.id = %s
            """, (pereval_id,))

            row = cur.fetchone()
            if not row:
                return None

            pereval = dict(row)

            cur.execute("""
                SELECT id, title, image_data
                FROM pereval_images
                WHERE pereval_id = %s
            """, (pereval_id,))

            images = []
            for img in cur.fetchall():
                img_dict = dict(img)
                img_dict["image_data"] = base64.b64encode(img_dict["image_data"]).decode("utf-8")
                images.append(img_dict)

            pereval["images"] = images
            return pereval

    def get_perevals_by_user_email(self, email: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT
                    p.id,
                    p.title,
                    p.add_time,
                    p.status
                FROM pereval_added p
                JOIN users u ON p.user_id = u.id
                WHERE u.email = %s
                ORDER BY p.add_time
            """, (email,))

            rows = cur.fetchall()
            return [dict(row) for row in rows]
