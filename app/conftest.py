import json
import pytest
from app import create_app, db
from app.models.portfolio import Portfolio
from app.models.investment import Investment
from app.models.portfolio_investment import PortfolioInvestment

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()

        # Load JSON data into the database
        with open("data/level_1/portfolios.json") as f:
            data = json.load(f)

        for contract in data["contracts"]:
            portfolio = Portfolio(
                label=contract["label"],
                type=contract["type"],
                amount=contract["amount"]
            )
            db.session.add(portfolio)
            db.session.flush()

            for line in contract.get("lines", []):
                investment = Investment.query.filter_by(isin=line["isin"]).first()
                if not investment:
                    investment = Investment(
                        type=line["type"],
                        isin=line["isin"],
                        label=line["label"],
                        price=line["price"],
                        srri=line["srri"]
                    )
                    db.session.add(investment)
                    db.session.flush()

                join_data = PortfolioInvestment(
                    portfolio_id=portfolio.id,
                    investment_id=investment.id,
                    amount=line["amount"],
                    share=line["share"]
                )
                db.session.add(join_data)

        db.session.commit()

    yield app.test_client()

    with app.app_context():
        db.drop_all()