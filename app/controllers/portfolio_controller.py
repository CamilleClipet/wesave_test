from flask import Blueprint, render_template, request

from app.business_logic.portfolio import invest_amount_in_portfolio

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/portfolios")


@portfolio_bp.route("/", methods=["GET"])
def get_portfolios():
    from app.models.portfolio import Portfolio

    portfolios = Portfolio.query.all()

    return render_template("portfolios.html", portfolios=portfolios)


@portfolio_bp.route("/deposit/<int:portfolio_id>", methods=["POST"])
def deposit_investment(portfolio_id):
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio

    data = request.get_json()
    amount = data.get("amount")
    investment_id = data.get("investment_id")

    if amount is None or amount <= 0:
        return "Invalid amount", 400

    portfolio = (
        Portfolio.query.get_or_404(portfolio_id)
    )
    if portfolio.type != "CTO" and portfolio.type != "PEA":
        return "Invalid portfolio type", 400
    
    investment = Investment.query.get_or_404(investment_id)

    invest_amount_in_portfolio(
        investment_id=investment.id, portfolio_id=portfolio.id, amount=amount
    )

    return "Investment deposited successfully", 200
