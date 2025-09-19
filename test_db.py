from app import create_app, db
from models.product import Product
from models.inventory import Inventory

app = create_app()

with app.app_context():
    db.create_all()
    try:
        product = Product(
            name="Widget Test",
            sku="WID-TEST",
            price=10.5,
            warehouse_id=1
        )
        db.session.add(product)
        db.session.commit()

        inventory = Inventory(
            product_id=product.id,
            warehouse_id=1,
            quantity=5
        )
        db.session.add(inventory)
        db.session.commit()

        print("Product inserted successfully:", product.id)

    except Exception as e:
        print("Error inserting product:", e)
