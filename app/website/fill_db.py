from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import DATABASE_URI
from models import (
    Base,
    Producer,
    CarModel,
    Country,
    Gearbox,
    Engine,
)

import requests
import json

marks_url = "https://auto.ria.com/api/categories/1/marks/_active/_with_count?langId=4&withNew=1"
models_url = "https://auto.ria.com/api/categories/1/marks/{mark_id}/models/_active/_with_count?langId=4&withNew=1"
gearboxes_url = "https://auto.ria.com/api/categories/1/gearboxes?langId=4"
fuel_url = "https://auto.ria.com/api/fuels?langId=4"
regions_url = "https://auto.ria.com/api/states?langId=4"
drives_url = "https://auto.ria.com/api/categories/1/driverTypes?langId=4"


def get_all_marks():
    marks_raw = requests.get(marks_url)
    marks = [(mark["name"], mark["value"]) for mark in json.loads(marks_raw.text.encode())]
    return marks
        

def get_all_models(session):
    marks = [(Producer(name=name), value) for (name, value) in get_all_marks()]
    
    try:
        marks_models = [mark[0] for mark in marks]
        session.add_all(marks_models)
        session.flush()

        for (producer, value) in marks:
            models_raw = requests.get(models_url.format(mark_id=value))
            models = [CarModel(name=model["name"], producer_id=producer.id) for model in json.loads(models_raw.text.encode())]
            session.add_all(models)
            session.flush()
        print("models done")
    except Exception as e:
        print(e)
        session.rollback()
           

def get_all_gearboxes(session):
    gearboxes_raw = requests.get(gearboxes_url)
    gearboxes = [Gearbox(name=gearbox["name"]) for gearbox in json.loads(gearboxes_raw.text.encode())]
    session.add_all(gearboxes)
    session.flush()
    print("gearboxes done")

def get_all_fuels(session):
    fuels_raw = requests.get(fuel_url)
    fuels = [Engine(name=fuel["name"]) for fuel in json.loads(fuels_raw.text.encode())]
    session.add_all(fuels)
    session.flush()
    print("fuels done")

def get_all_regions(session):
    regions_raw = requests.get(regions_url)
    regions = [Country(name=region["name"]) for region in json.loads(regions_raw.text.encode())]
    session.add_all(regions)
    session.flush()
    print("regions done")


def create_db():
    engine = create_engine(DATABASE_URI)

    session = Session(engine)
    session.query(CarModel).delete()
    session.query(Producer).delete()
    session.query(Engine).delete()
    session.query(Gearbox).delete()
    session.query(Country).delete()
    session.flush()
    session.commit()

    get_all_models(session)
    get_all_gearboxes(session)
    get_all_fuels(session)
    get_all_regions(session)
    session.commit()

if __name__ == "__main__":
    create_db()