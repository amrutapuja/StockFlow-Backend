from flask import Blueprint, jsonify
from app import db
from models.company import Company
from models.warehouse import Warehouse
from models.inventory import Inventory
from models.product import Product
from models.supplier import Supplier, SupplierProduct
from models.sales import Sale
from datetime import datetime, timedelta
from sqlalchemy import func
import math

alerts_bp = Blueprint("alerts", __name__, url_prefix="/api/companies")

RECENT_DAYS = 30

@alerts_bp.route("/<int:company_id>/alerts/low-stock", methods=["GET"])
def low_stock_alerts(company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({"error": "company not found"}), 404

    warehouses = Warehouse.query.filter_by(company_id=company_id).all()
    if not warehouses:
        return jsonify({"alerts": [], "total_alerts": 0})

    warehouse_ids = [w.id for w in warehouses]
    now = datetime.utcnow()
    window_start = now - timedelta(days=RECENT_DAYS)

    sales_subq = db.session.query(
        Sales.product_id,
        Sales.warehouse_id,
        func.sum(Sales.quantity).label("qty_sold")
    ).filter(
        Sales.sold_at >= window_start,
        Sales.warehouse_id.in_(warehouse_ids)
    ).group_by(Sales.product_id, Sales.warehouse_id).subquery()

    joined = db.session.query(
        Inventory,
        Product,
        Warehouse,
        sales_subq.c.qty_sold
    ).join(Product, Inventory.product_id == Product.id) \
     .join(Warehouse, Inventory.warehouse_id == Warehouse.id) \
     .join(sales_subq, (sales_subq.c.product_id == Inventory.product_id) &
                       (sales_subq.c.warehouse_id == Inventory.warehouse_id))

    alerts = []
    for inv, product, warehouse, qty_sold in joined:
        threshold = product.low_stock_threshold or 0
        current_stock = inv.quantity
        if current_stock >= threshold:
            continue

        avg_daily_sales = qty_sold / RECENT_DAYS if RECENT_DAYS > 0 else 0
        if avg_daily_sales <= 0:
            continue

        days_until_stockout = math.floor(current_stock / avg_daily_sales) if avg_daily_sales > 0 else None

        sp = SupplierProduct.query.filter_by(product_id=product.id, is_primary=True).first()
        supplier_info = None
        if sp:
            supplier = Supplier.query.get(sp.supplier_id)
            if supplier:
                supplier_info = {
                    "id": supplier.id,
                    "name": supplier.name,
                    "contact_email": supplier.contact_email
                }

        alerts.append({
            "product_id": product.id,
            "product_name": product.name,
            "sku": product.sku,
            "warehouse_id": warehouse.id,
            "warehouse_name": warehouse.name,
            "current_stock": current_stock,
            "threshold": threshold,
            "days_until_stockout": days_until_stockout,
            "supplier": supplier_info
        })

    return jsonify({"alerts": alerts, "total_alerts": len(alerts)})
