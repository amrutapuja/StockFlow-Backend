from app import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    product_type = db.Column(db.String(50), nullable=True)

    # ✅ add threshold
    low_stock_threshold = db.Column(db.Integer, nullable=False, default=5)

    inventories = db.relationship("Inventory", backref="product", lazy=True)
    sales = db.relationship("Sale", backref="product", lazy=True)
