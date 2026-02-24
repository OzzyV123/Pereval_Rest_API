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

@app.post("/submitData")
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

@app.get("/submitData/{pereval_id}")
def get_submit_data(pereval_id: int):
    pereval = db.get_pereval_by_id(pereval_id)

    if not pereval:
        raise HTTPException(
            status_code=404,
            detail="Перевал с таким id не найден"
        )

    return pereval

@app.get("/submitData/")
def get_submit_data_by_user(user__email: Optional[str] = Query(None)):
    if not user__email:
        return []

    return db.get_perevals_by_user_email(user__email)
