from app import db
from datetime import datetime

class Sale(db.Model):   # ✅ rename from Sales to Sale
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"))
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.DECIMAL(12, 2))
    sold_at = db.Column(db.DateTime, default=datetime.utcnow)
