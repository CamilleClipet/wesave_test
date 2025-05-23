from flask import Blueprint, render_template, request

from app.business_logic.portfolio import (
    invest_amount_in_portfolio,
    move_money_between_investments,
    withdraw_amount_from_portfolio,
)

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

    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.type != "CTO" and portfolio.type != "PEA":
        return "Invalid portfolio type", 400

    investment = Investment.query.get_or_404(investment_id)

    invest_amount_in_portfolio(
        investment_id=investment.id, portfolio_id=portfolio.id, amount=amount
    )

    return "Investment deposited successfully", 200


@portfolio_bp.route("/withdraw/<int:portfolio_id>", methods=["POST"])
def withdraw_investment(portfolio_id):
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio

    data = request.get_json()
    amount = data.get("amount")
    investment_id = data.get("investment_id")

    if amount is None or amount <= 0:
        return "Invalid amount", 400

    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.type != "CTO" and portfolio.type != "PEA":
        return "Invalid portfolio type", 400

    investment = Investment.query.get_or_404(investment_id)

    try:
        withdraw_amount_from_portfolio(
            investment_id=investment.id, portfolio_id=portfolio.id, amount=amount
        )
    except ValueError as e:
        if str(e) == "Investment not found in portfolio":
            return "Investment not found in portfolio", 404
        elif str(e) == "Not enough amount to withdraw":
            return "Not enough amount to withdraw", 400
        else:
            return "An unexpected error occurred", 500

    return "Investment withdrawn successfully", 200


@portfolio_bp.route("/move/<int:portfolio_id>", methods=["POST"])
def _move_money_between_investments(portfolio_id):
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    data = request.get_json()
    amount = data.get("amount")
    investment_id_from = data.get("investment_id_from")
    investment_id_to = data.get("investment_id_to")

    if amount is None or amount <= 0:
        return "Invalid amount", 400

    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.type != "CTO" and portfolio.type != "PEA":
        return "Invalid portfolio type", 400

    investment_from = Investment.query.get_or_404(investment_id_from)
    investment_to = Investment.query.get_or_404(investment_id_to)

    try:
        move_money_between_investments(
            investment_id_from=investment_from.id,
            investment_id_to=investment_to.id,
            portfolio_id=portfolio_id,
            amount=amount,
        )
    except ValueError as e:
        if str(e) == "Investment not found in portfolio":
            return "Investment not found in portfolio", 404
        elif str(e) == "Not enough amount to withdraw":
            return "Not enough amount to withdraw", 400
        else:
            return "An unexpected error occurred", 500

    return "Money moved successfully", 200
