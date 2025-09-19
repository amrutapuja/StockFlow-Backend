def test_create_product(client):
    payload = {"name": "TestProd", "sku": "SKU123", "price": "99.99"}
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
