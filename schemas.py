from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str

class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int

class Level(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class Image(BaseModel):
    data: str
    title: Optional[str] = None

class Pereval(BaseModel):
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: Optional[str] = None

    user: User
    coords: Coords
    level: Level
    images: List[Image]