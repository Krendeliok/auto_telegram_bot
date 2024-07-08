from flask import (
    Response,
    request,
    g
)
from flask_restful import Resource

from models import (
    Advertisement,
    AditionalAdvertisements,
    AdvertisementStateEnum,
    AdvertisementKindEnum,
    Client,
    Producer,
    Engine,
    Gearbox,
    CarModel,
    Image,
)

from sqlalchemy.sql import expression
from sqlalchemy import func, desc, asc

import json

def list_from_args(args: dict, list_name: str):
    res = args.get(list_name)
    return list(map(int, res.split(","))) if res else []

def range_from_args(args: dict, range_name: str, is_float: bool = False):
    convert_type = float if is_float else int
    return {
        "cleft": convert_type(args.get(f"{range_name}_min", 0)), 
        "cright": convert_type(args.get(f"{range_name}_max", 0))
    }

def parse_sort(sort):
    if "cheapest" == sort:
        return asc(Advertisement.price)
    if "expensive" == sort:
        return desc(Advertisement.price)
    if "new" == sort:
        return desc(Advertisement.year)

    return asc(Advertisement.id)

class AdvertisementsApi(Resource):
    def get(self, id=None):
        advs = (
            g.db
            .query(Advertisement)
        )
        if id:
            advs = advs.filter(Advertisement.id == id)
        advs = advs.all()
        result = [
            {
                "id": adv.id,
                "client_telegram_id": adv.client.telegram_id,
                "producer": adv.model.producer.name,
                "model": adv.model.name,
                "year": adv.year,
                "engine_type": adv.engine.name,
                "engine_volume": str(adv.engine_volume),
                "gearbox_type": adv.gearbox.name,
                "range": adv.range,
                "based_country": adv.country.name,
                "description": adv.description,
                "price": adv.price,
                "phone_number": adv.phone_number if adv.phone_number else adv.client.phone_number,
                "images": [
                    { 
                        "id": image.id,
                        "source": image.source,
                        "cloudinary_source": image.cloudinary_source
                    } for image in adv.images
                ]
            } for adv in advs
        ]
        return Response(json.dumps(result, default=str), mimetype="application/json")

    def post(self):
        try:
            data = request.json
            user = g.db.query(Client).filter_by(telegram_id=data["user_id"]).first()

            data["phone_number"] = data.get("phone", user.phone_number)
            data["phone_number"] = data["phone_number"] if str(data["phone_number"]).startswith("+") else f"+{data['phone_number']}"

            adv = Advertisement(
                user_id=user.id,
                model_id=data["model_id"],
                price=data["price"],
                year=data["year"],
                engine_type_id=data["engine_type_id"],
                engine_volume=data["engine_volume"],
                range=data["range"],
                gearbox_type_id=data["gearbox_type_id"],
                based_country_id=data["based_country_id"],
                phone_number=data["phone_number"],
                description=data["description"],
                vin=data["vin"],
                kind=data["kind"]
            )

            if data["kind"] == AdvertisementKindEnum.additional.value:
                additional_adv: AditionalAdvertisements = (
                    g.db
                    .query(AditionalAdvertisements)
                    .filter(
                        AditionalAdvertisements.client_id == user.id,
                        AditionalAdvertisements.reserved == expression.false()
                    ).first()
                )

                additional_adv.advertisement = adv
                g.db.add(additional_adv)
                additional_adv.update_expires_dates()
                g.db.flush()
            g.db.add(adv)
            g.db.flush()
            adv.update_publishing_dates()
            images = [
                Image(
                    advertisement_id=adv.id,
                    source=image["source"],
                    cloudinary_source=image["cloudinary_source"]
                ) for image in data["images"]
            ]
            g.db.add_all(images)
            g.db.commit()

            return Response(json.dumps({"ok": True, "adv_id": adv.id}, default=str), mimetype="application/json")
        except Exception as ex:
            return Response(json.dumps({"ok": False, "message": ex}, default=str), mimetype="application/json", status=400)

class PriceApi(Resource):
    def get(self):
        res, *_ = (
            g.db
            .query(func.max(Advertisement.price))
            .join(Client, Advertisement.user_id == Client.id)
            .filter(
                expression.or_(Client.is_admin, Client.is_owner),
                Advertisement.status == AdvertisementStateEnum.approved
                )
            .all()
        )
        
        return Response(json.dumps(res[0], default=str), mimetype="application/json")
    
class AdminAdvertisements(Resource):
    def get(self):
        limit = int(request.args.get("_limit", 0))
        page = int(request.args.get("_page", 1))
        producers = list_from_args(request.args, "_producers")
        fuels = list_from_args(request.args, "_fuels")
        gearboxes = list_from_args(request.args, "_gearboxes")
        sort = parse_sort(request.args.get("_sort_by"))

        filters = []
        joins = []
        if fuels:
            filters.append(Engine.id.in_(fuels))
            joins.append((Engine, Advertisement.engine_type_id == Engine.id))
        if gearboxes:
            filters.append(Gearbox.id.in_(gearboxes))
            joins.append(
                (Gearbox, Advertisement.gearbox_type_id == Gearbox.id))
        if producers:
            filters.append(Producer.id.in_(producers))
            joins.append((CarModel, Advertisement.model_id == CarModel.id))
            joins.append((Producer, CarModel.producer_id == Producer.id))

        price = range_from_args(request.args, "_price")
        year = range_from_args(request.args, "_year")
        range_ = range_from_args(request.args, "_range")
        engine_volume = range_from_args(request.args, "_engine_volume", True)
        headers = []
        advs = (
            g.db
            .query(Advertisement)
            .join(Client, Advertisement.user_id == Client.id)
        )
        for join_ in joins:
            advs = advs.join(*join_)

        advs = advs.filter(
            expression.or_(Client.is_admin, Client.is_owner),
            Advertisement.status == AdvertisementStateEnum.approved,
            Advertisement.price.between(**price),
            Advertisement.year.between(**year),
            Advertisement.range.between(**range_),
            Advertisement.engine_volume.between(**engine_volume),
            *filters
        )

        advs = advs.order_by(sort)

        if any([limit, page]):
            headers.append(("x-total-count", advs.count()))
        if limit:
            advs = advs.limit(limit * page)
        advs = advs.all()
        result = [
            {
                "id": adv.id,
                "producer": adv.model.producer.name,
                "model": adv.model.name,
                "year": adv.year,
                "engine_type": adv.engine.name,
                "engine_volume": str(adv.engine_volume),
                "gearbox_type": adv.gearbox.name,
                "range": adv.range,
                "based_country": adv.country.name,
                "description": adv.description,
                "price": adv.price,
                "images": [
                    {
                        "id": image.id,
                        "source": image.cloudinary_source
                    } for image in adv.images
                ]
            } for adv in advs
        ]
        return Response(json.dumps(result, default=str), mimetype="application/json", headers=headers)
