from flask import (
    Response,
    g
)
from flask_restful import Resource

from models import (
    Producer
)

import json

class ProducersApi(Resource):
    def get(self):
        producers = g.db.query(Producer).all()
        result = [
            {
                "id": producer.id,
                "name": producer.name,
            } for producer in producers
        ]
        return Response(json.dumps(result, default=str), mimetype="application/json")