from views.index import index_bp

def route(app):
    app.register_blueprint(index_bp)