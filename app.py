from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from models import company, warehouse, product, inventory, supplier, sales

    from routes.products import products_bp
    from routes.alerts import alerts_bp

    app.register_blueprint(products_bp)
    app.register_blueprint(alerts_bp)

    @app.route("/")
    def home():
        return {"message": "StockFlow Backend is running!"}

    with app.app_context():
        db.create_all()

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
