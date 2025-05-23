import json

from app import create_app, db
from app.models.portfolio import Portfolio
from app.models.investment import Investment
from app.models.portfolio_investment import PortfolioInvestment

app = create_app()

with app.app_context():
    with open("data/level_1/portfolios.json") as f:
        data = json.load(f)

    for contract in data["contracts"]:
        portfolio = Portfolio(
            label=contract["label"],
            type=contract["type"],
            amount=contract["amount"],
        )
        db.session.add(portfolio)
        db.session.flush()

        for line in contract.get("lines", []):
            inv = Investment.query.filter_by(isin=line["isin"]).first()
            if not inv:
                inv = Investment(
                    type=line["type"],
                    isin=line["isin"],
                    label=line["label"],
                    price=line["price"],
                    srri=line["srri"],
                )
                db.session.add(inv)
                db.session.flush()

            assoc = PortfolioInvestment(
                portfolio_id=portfolio.id,
                investment_id=inv.id,
                amount=line["amount"],
                share=line["share"],
            )
            db.session.add(assoc)

    db.session.commit()
