from flask import (
    Response,
    g
)
from flask_restful import Resource

from models import (
    Gearbox
)

import json

class GearboxApi(Resource):
    def get(self):
        gearboxes = g.db.query(Gearbox).all()
        result = [
            {
                "id": gearbox.id,
                "name": gearbox.name,
            } for gearbox in gearboxes
        ]
        return Response(json.dumps(result, default=str), mimetype="application/json")