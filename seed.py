from app import create_app, db
from models.company import Company
from models.warehouse import Warehouse
from models.product import Product
from models.inventory import Inventory
from models.supplier import Supplier, SupplierProduct
from models.sales import Sales

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    c1 = Company(name="Acme Inc.")
    db.session.add(c1)
    db.session.flush()

    w1 = Warehouse(name="Main Warehouse", company_id=c1.id)
    db.session.add(w1)

    p1 = Product(name="Widget A", sku="WID-001", price=10.50, low_stock_threshold=20)
    db.session.add(p1)
    db.session.flush()

    inv1 = Inventory(product_id=p1.id, warehouse_id=w1.id, quantity=5)
    db.session.add(inv1)

    s1 = Supplier(name="Supplier Corp", contact_email="orders@supplier.com")
    db.session.add(s1)
    db.session.flush()

    sp1 = SupplierProduct(supplier_id=s1.id, product_id=p1.id, is_primary=True, lead_time_days=7)
    db.session.add(sp1)

    sale = Sales(product_id=p1.id, warehouse_id=w1.id, quantity=10, total_price=105.00)
    db.session.add(sale)

    db.session.commit()
    print("Database seeded ✅")
