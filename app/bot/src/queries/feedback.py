from ..Api.Request import Request


async def get_not_verified_feedbacks() -> list[dict]:
    params = {
        "verified": "false"
    }
    response = await Request.get("feedbacks", params=params)
    return list(response)


async def set_verified_feedback(id: int):
    await Request.put(f"feedbacks/{id}", body={"verified": "true"})