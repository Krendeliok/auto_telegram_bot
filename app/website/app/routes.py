from api.advertisements import Advertisements

def route(api):
    api.add_resource(Advertisements, "/api/v1/advertisements")