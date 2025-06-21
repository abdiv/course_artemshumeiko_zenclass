from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    name: str


class HotelPATCH(BaseModel):
    title: str | None = Field(None)  # Обязательно задавать значения по умолчанию!
    name: str | None = Field(None)