from flask import (
    Response,
    request,
    g
)
from flask_restful import Resource

from models import (
    Feedback
)

import json


class FeedbackApi(Resource):
    def get(self):
        feedbacks = g.db.query(Feedback).filter_by(**request.args).all()
        result = [feedback.as_dict() for feedback in feedbacks]
        return Response(json.dumps(result, default=str), mimetype="application/json")
    def post(self):
        try:
            data = request.json
            name = data["name"] or None
            phone = data["phone"] or None

            if not all([name, phone]):
                raise ValueError("Any of [name, phone] not specified")

            advertisement_id = data.get("advertisement_id", None)
            if advertisement_id:
                advertisement_id = int(advertisement_id)
            new_feedback = Feedback(name=name, phone=phone, advertisement_id=advertisement_id)
            g.db.add(new_feedback)
            g.db.commit()
            return Response(json.dumps({"ok": True, "feedback_id": new_feedback.id}, default=str), mimetype="application/json")
        except Exception as ex:
            return Response(json.dumps({"ok": False, "message": ex}, default=str), mimetype="application/json", status=400)

    def put(self, id):
        try:
            data = request.json
            feedback = g.db.query(Feedback).filter_by(id=id).first()
            if "name" in data:
                feedback.name = data.pop("name")
            if "phone" in data:
                feedback.phone = data.pop("phone")
            if "verified" in data:
                feedback.verified = True if data.pop("verified") == "true" else False
            g.db.add(feedback)
            g.db.commit()
            return Response(json.dumps({"ok": True, "feedback_id": feedback.id}, default=str), mimetype="application/json")
        except Exception as ex:
            return Response(json.dumps({"ok": False, "message": ex}, default=str), mimetype="application/json", status=400)
