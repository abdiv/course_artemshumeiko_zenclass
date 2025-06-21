from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("",
    summary="Отели",
    description="Отображение списка всех отелей, либо посмотр информации по одному отелю по id и/или title")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(1, ge=1, description="Номер страницы"),
        per_page: int | None = Query(2, ge=1, le=len(hotels), description="Количество элементов на странице"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[(page-1)*per_page:per_page*page]


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Удаление отеля по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


#body, request body
@router.post(
    "",
    summary="Добавление отеля",
    description="Добавление нового отеля при отправке title")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "name": "dubai_fountain",
    }},
})):
    global hotels
    hotels.append({
            "id": hotels[-1]["id"] + 1,
            "title": hotel_data.title,
            "name": hotel_data.name,
      })
    return {"status": "OK"}


def find_hotel_id(hotel_id: int):
    """Проверка наличия отеля по ID"""
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            return hotel
    return None


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных об отеле",
    description="Изменение title и name по id отеля")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    hotel = find_hotel_id(hotel_id)
    if hotel is not None:
        hotel.update({
            "title": hotel_data.title,
            "name": hotel_data.name
        })
        return hotel
    else:
        return {"status": "Fail",
                "description": "Такого hotel_id не существует"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Изменение title или name или title+name по id отеля")
def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        ):
    hotel = find_hotel_id(hotel_id)
    if hotel is not None:
        if hotel_data.title is not None or hotel_data.name is not None:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return hotel
        else:
            return {"status": "Fail",
                    "description": "Нет данных для изменения"}
    else:
        return {"status": "Fail",
                "description": "Такого hotel_id не существует"}

