from flask import Blueprint, request, jsonify
from app import db
from models.product import Product
from models.inventory import Inventory
from models.warehouse import Warehouse
from sqlalchemy.exc import IntegrityError
from decimal import Decimal, InvalidOperation
import traceback

products_bp = Blueprint("products", __name__, url_prefix="/api/products")

@products_bp.route("", methods=["POST"])
def create_product():
    data = request.get_json() or {}

    print("DEBUG JSON received:", data)

    required = ["name", "sku", "price"]
    for f in required:
        if f not in data:
            return jsonify({"error": f"'{f}' is required"}), 400

    price_value = data.get("price")
    if price_value is None:
        return jsonify({"error": "'price' is required"}), 400

    try:
        price = Decimal(str(price_value))
    except (InvalidOperation, TypeError):
        return jsonify({"error": "invalid price"}), 400

    warehouse_id = data.get("warehouse_id")
    initial_qty = data.get("initial_quantity", 0)
    low_stock_threshold = data.get("low_stock_threshold", 5)

    try:
        with db.session.begin():
            product = Product(
                name=data["name"].strip(),
                sku=data["sku"].strip(),
                price=price,
                low_stock_threshold=low_stock_threshold
            )
            db.session.add(product)
            db.session.flush()

            if warehouse_id:
                wh = Warehouse.query.get(warehouse_id)
                if not wh:
                    raise ValueError("warehouse_id does not exist")

                if not isinstance(initial_qty, int) or initial_qty < 0:
                    raise ValueError("initial_quantity must be integer >= 0")

                inv = Inventory(
                    product_id=product.id,
                    warehouse_id=warehouse_id,
                    quantity=initial_qty
                )
                db.session.add(inv)

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "SKU already exists"}), 409
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({"error": f"{type(e).__name__}: {str(e)}"}), 500

    return jsonify({"message": "Product created", "product_id": product.id}), 201
