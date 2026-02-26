from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Optional
import base64

from db import PerevalDB
from schemas import Pereval

app = FastAPI(title="FSTR Pereval API")

db = PerevalDB()

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "message": "Bad Request: missing or invalid fields",
            "id": None,
        },
    )

@app.post("/submitData",
          summary="Добавить новый перевал",
          description="Принимает данные о перевале, пользователе, координатах и изображениях.",
          responses={
              200: {
                  "description": "Успешно",
                  "content": {
                      "application/json": {
                          "example": {"status": 200, "message": None, "id": 42}
                      }
                  }
              },
              400: {"description": "Неверные данные"},
              500: {"description": "Ошибка сервера"},
          },
          )
def submit_data(pereval: Pereval):
    try:
        # пользователь
        user_id = db.add_user(
            email=pereval.user.email,
            fam=pereval.user.fam,
            name=pereval.user.name,
            otc=pereval.user.otc,
            phone=pereval.user.phone,
        )

        # координаты
        coord_id = db.add_coords(
            latitude=pereval.coords.latitude,
            longitude=pereval.coords.longitude,
            height=pereval.coords.height,
        )

        # перевал
        pereval_id = db.add_pereval(
            beauty_title=pereval.beauty_title,
            title=pereval.title,
            other_titles=pereval.other_titles,
            connect=pereval.connect,
            user_id=user_id,
            coord_id=coord_id,
            level_winter=pereval.level.winter,
            level_summer=pereval.level.summer,
            level_autumn=pereval.level.autumn,
            level_spring=pereval.level.spring,
        )

        # изображения
        for image in pereval.images:
            image_bytes = base64.b64decode(image.data)
            db.add_image(
                pereval_id=pereval_id,
                image_data=image_bytes,
                title=image.title,
            )

        return {
            "status": 200,
            "message": None,
            "id": pereval_id,
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": str(e),
                "id": None,
            },
        )

@app.get("/submitData/{pereval_id}",
         summary="Получить информацию о перевале",
         description="Выводит данные о перевале с данным id.",
         responses={
             200: {
                 "description": "Перевал найден",
                 "content": {
                     "application/json": {
                         "example": {
                             "id": 7,
                             "beauty_title": "пер.",
                             "title": "Пхия",
                             "other_titles": "Триев",
                             "connect": "",
                             "add_time": "2021-09-22 13:18:13",
                             "status": "new",
                             "email": "user@mail.ru",
                             "fam": "Пупкин",
                             "name": "Василий",
                             "otc": "Иванович",
                             "phone": "+7 555 55 55",
                             "latitude": 45.3842,
                             "longitude": 7.1525,
                             "height": 1200,
                             "level_winter": "",
                             "level_summer": "1А",
                             "level_autumn": "1А",
                             "level_spring": "",
                             "images": [
                                 {
                                     "id": 1,
                                     "title": "Седловина",
                                     "image_data": "<base64>"
                                 }
                             ]
                         }
                     }
                 }
             },
             404: {
                 "description": "Перевал не найден",
                 "content": {
                     "application/json": {
                         "example": {"detail": "Перевал с таким id не найден"}
                     }
                 }
             },
             500: {"description": "Ошибка сервера"},
         },
         )
def get_submit_data(pereval_id: int):
    pereval = db.get_pereval_by_id(pereval_id)

    if not pereval:
        raise HTTPException(
            status_code=404,
            detail="Перевал с таким id не найден"
        )

    return pereval

@app.get("/submitData/",
         summary="Получить информацию о перевалах пользователя",
         description="Выводит данные о всех перевала пользователя с данной почтой.",
         responses={
             200: {
                 "description": "Список перевалов",
                 "content": {
                     "application/json": {
                         "example": [
                             {
                                 "id": 3,
                                 "title": "Пхия",
                                 "add_time": "2021-09-22 13:18:13",
                                 "status": "accepted"
                             },
                             {
                                 "id": 7,
                                 "title": "Тестовый перевал",
                                 "add_time": "2023-10-01 12:00:00",
                                 "status": "new"
                             }
                         ]
                     }
                 }
             },
             500: {"description": "Ошибка сервера"},
         },
         )
def get_submit_data_by_user(user__email: Optional[str] = Query(None)):
    if not user__email:
        return []

    return db.get_perevals_by_user_email(user__email)

@app.patch("/submitData/{pereval_id}",
           summary="Изменить существующий перевал",
           description="Позволяет изменить данные о перевале (кроме данных пользователя). Нельзя изменить если статус перевала не new.",
           responses={
               200: {
                   "description": "Успешно обновлено",
                   "content": {
                       "application/json": {
                           "example": {
                               "state": 1,
                               "message": "Запись успешно обновлена"
                           }
                       }
                   }
               },
               400: {
                   "description": "Редактирование запрещено",
                   "content": {
                       "application/json": {
                           "example": {
                               "state": 0,
                               "message": "Редактирование запрещено: статус не 'new'"
                           }
                       }
                   }
               },
               404: {
                   "description": "Перевал не найден",
                   "content": {
                       "application/json": {
                           "example": {
                               "state": 0,
                               "message": "Перевал не найден"
                           }
                       }
                   }
               },
               500: {"description": "Ошибка сервера"},
           },
           )
def patch_submit_data(pereval_id: int, pereval: Pereval):
    status = db.get_pereval_status(pereval_id)

    if status is None:
        return {
            "state": 0,
            "message": "Перевал не найден"
        }

    if status != "new":
        return {
            "state": 0,
            "message": "Редактирование запрещено: статус не new"
        }

    try:
        db.update_pereval(pereval_id, pereval)
        db.replace_images(pereval_id, pereval.images)

        return {
            "state": 1,
            "message": "ok"
        }

    except Exception as e:
        return {
            "state": 0,
            "message": str(e)
        }
