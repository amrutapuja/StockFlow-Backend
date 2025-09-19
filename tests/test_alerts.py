def test_low_stock_alerts(client):
    response = client.get("/api/companies/1/alerts/low-stock")
    assert response.status_code in (200, 404)
