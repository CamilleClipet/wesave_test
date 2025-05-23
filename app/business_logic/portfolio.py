def invest_amount_in_portfolio(investment_id, portfolio_id, amount):
    from app import db
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    portfolio = Portfolio.query.get(portfolio_id)

    # check if investment already in portfolio
    portfolio_investment = PortfolioInvestment.query.filter_by(
        investment_id=investment_id, portfolio_id=portfolio_id
    ).first()

    if portfolio_investment:
        portfolio_investment.amount += amount
    else:
        portfolio_investment = PortfolioInvestment(
            portfolio_id=portfolio_id,
            investment_id=investment_id,
            amount=amount,
            share=0,  # share will be calculated later
        )
        db.session.add(portfolio_investment)

    new_total_amount = portfolio.amount + amount
    portfolio.amount = new_total_amount

    for investment in portfolio.portfolio_investments:
        investment.share = (
            investment.amount / new_total_amount if new_total_amount > 0 else 0
        )

    db.session.commit()


def withdraw_amount_from_portfolio(investment_id, portfolio_id, amount):
    from app import db
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    portfolio = Portfolio.query.get(portfolio_id)

    # check if investment already in portfolio
    portfolio_investment = PortfolioInvestment.query.filter_by(
        investment_id=investment_id, portfolio_id=portfolio_id
    ).first()

    if not portfolio_investment:
        raise ValueError("Investment not found in portfolio")

    if portfolio_investment.amount < amount:
        raise ValueError("Not enough amount to withdraw")

    portfolio_investment.amount -= amount

    new_total_amount = portfolio.amount - amount
    portfolio.amount = new_total_amount

    for investment in portfolio.portfolio_investments:
        investment.share = (
            investment.amount / new_total_amount if new_total_amount != 0 else 0
        )

    db.session.commit()


def move_money_between_investments(
    investment_id_from, investment_id_to, portfolio_id, amount
):
    from app import db
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    portfolio = Portfolio.query.get(portfolio_id)

    # check if investment already in portfolio
    portfolio_investment_from = PortfolioInvestment.query.filter_by(
        investment_id=investment_id_from, portfolio_id=portfolio_id
    ).first()

    if not portfolio_investment_from:
        raise ValueError("Investment not found in portfolio")

    if portfolio_investment_from.amount < amount:
        raise ValueError("Not enough amount to withdraw")

    # check if investment already in portfolio
    portfolio_investment_to = PortfolioInvestment.query.filter_by(
        investment_id=investment_id_to, portfolio_id=portfolio_id
    ).first()

    if not portfolio_investment_to:
        raise ValueError("Investment not found in portfolio")

    portfolio_investment_from.amount -= amount
    portfolio_investment_to.amount += amount

    for investment in portfolio.portfolio_investments:
        investment.share = (
            investment.amount / portfolio.amount if portfolio.amount != 0 else 0
        )

    db.session.commit()
