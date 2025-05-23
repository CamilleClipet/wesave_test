from flask import Blueprint, render_template

portfolio_bp = Blueprint("portfolio", __name__, url_prefix="/portfolios")


@portfolio_bp.route("/", methods=["GET"])
def get_portfolios():
    from app.models.portfolio import Portfolio

    portfolios = Portfolio.query.all()

    return render_template("portfolios.html", portfolios=portfolios)
