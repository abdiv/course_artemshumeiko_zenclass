import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]


@app.get(
    "/hotels",
    summary="Отели",
    description="Отображение списка всех отелей, либо посмотр информации по одному отелю по id и/или title")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.delete(
    "/hotels/{hotel_id}",
    summary="Удаление отеля",
    description="Удаление отеля по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


#body, request body
@app.post(
    "/hotels",
    summary="Добавление отеля",
    description="Добавление нового отеля при отправке title")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
            "id": hotels[-1]["id"] + 1,
            "title": title
      })
    return {"status": "OK"}


def find_hotel_id(hotel_id: int):
    """Проверка наличия отеля по ID"""
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return hotel
    return None


@app.put(
    "/hotels/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Изменение title и name по id отеля")
def put_hotel(
        hotel_id: int,
        title: str = Body(),
        name: str = Body()
        ):
    hotel = find_hotel_id(hotel_id)
    if hotel is not None:
        hotel.update({
            "title": title,
            "name": name
        })
        return hotel
    else:
        return {"status": "Fail",
                "description": "Такого hotel_id не существует"}


@app.patch(
    "/hotels/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Изменение title или name или title+name по id отеля")
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None)
        ):
    hotel = find_hotel_id(hotel_id)
    if hotel is not None:
        if title is not None or name is not None:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return hotel
        else:
            return {"status": "Fail",
                    "description": "Нет данных для изменения"}
    else:
        return {"status": "Fail",
                "description": "Такого hotel_id не существует"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, reload_delay=2)
