from flask import (
    Response,
    g
)
from flask_restful import Resource

from models import (
    Engine
)

import json

class EngineApi(Resource):
    def get(self):
        engines = g.db.query(Engine).all()
        result = [
            {
                "id": engine.id,
                "name": engine.name,
            } for engine in engines
        ]
        return Response(json.dumps(result, default=str), mimetype="application/json")