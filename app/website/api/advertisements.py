from flask import (
    Response,
)
from flask_restful import Resource

import json

cards = [
    {
        "id": 1,
        "producer": "BMW",
        "model": "M3",
        "year": 2003,
        "engine_type": "Дизель",
        "engine_volume": 1.9,
        "gearbox_type": "Механіка",
        "range": 100,
        "based_country": "Закарпатська",
        "description": "Авто із Чехії, приведене до ладу. Перебрана ходова, питань по мотору та коробці нема, масло не бере, повторний окрас капоту, є комплект шин, нюанс по лобовому склу.",
        "price": 200000,
        "images": [
            { "id": 1, "source": "../../assets/second_car.png" },
            { "id": 2, "source": "../../assets/avto.png" },
            { "id": 3, "source": "../../assets/avto.png" },
        ]
    },
    {
        "id": 2,
        "producer": "BMW",
        "model": "M3",
        "year": 2003,
        "engine_type": "Дизель",
        "engine_volume": 1.9,
        "gearbox_type": "Механіка",
        "range": 100,
        "based_country": "Закарпатська",
        "description": "Авто із Чехії, приведене до ладу. Перебрана ходова, питань по мотору та коробці нема, масло не бере, повторний окрас капоту, є комплект шин, нюанс по лобовому склу.",
        "price": 200000,
        "images": [
            { "id": 4, "source": "../../assets/second_car.png" },
            { "id": 5, "source": "../../assets/avto.png" },
            { "id": 6, "source": "../../assets/avto.png" },
        ]
    },
]

class Advertisements(Resource):
    def get(self):
        return Response(json.dumps(cards, default=str), mimetype="application/json")