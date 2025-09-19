from app import db

class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(50))


class SupplierProduct(db.Model):
    __tablename__ = "supplier_products"

    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    lead_time_days = db.Column(db.Integer)
    cost_price = db.Column(db.DECIMAL(12, 2))
    is_primary = db.Column(db.Boolean, default=False)
