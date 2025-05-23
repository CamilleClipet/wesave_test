import pytest

@pytest.mark.unit
def test_portfolio_response(client):
    response = client.get("/portfolios/")
    assert response.status_code == 200
    assert b"Compte courant" in response.data
    html = response.data.decode("utf-8")
    assert "<table" in html
    assert "<th>Label</th>" in html
