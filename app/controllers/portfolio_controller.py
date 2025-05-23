from flask import Blueprint, jsonify

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/portfolios")


@portfolio_bp.route("/", methods=["GET"])
def get_portfolios():
    from app.models.portfolio import Portfolio

    portfolios = Portfolio.query.all()

    result = []
    for portfolio in portfolios:
        portfolio_data = {
            "label": portfolio.label,
            "type": portfolio.type,
            "amount": portfolio.amount,
            "investments": [],
        }

        for portfolio_investment in portfolio.portfolio_investments:
            investment = portfolio_investment.investment
            investment_data = {
                "type": investment.type,
                "isin": investment.isin,
                "label": investment.label,
                "price": investment.price,
                "srri": investment.srri,
                "amount": portfolio_investment.amount,
                "share": portfolio_investment.share,
            }
            portfolio_data["investments"].append(investment_data)

        result.append(portfolio_data)

    return jsonify(result)
