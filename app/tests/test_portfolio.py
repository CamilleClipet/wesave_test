import pytest


@pytest.mark.unit
def test_portfolio_response(client):
    response = client.get("/portfolios/")
    assert response.status_code == 200
    assert b"Compte courant" in response.data
    html = response.data.decode("utf-8")
    assert "<table" in html
    assert "<th>Label</th>" in html


@pytest.mark.unit
def test_deposit_investment_successfully(client):
    from app.business_logic.portfolio import invest_amount_in_portfolio
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    with client.application.app_context():
        portfolio = Portfolio.query.first()  # is a CTO
        assert portfolio is not None
        initial_amount = portfolio.amount

        # we want to invest in investment labelled "Apple Inc."
        target_investment = Investment.query.filter_by(label="Apple Inc.").first()
        apple_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=target_investment.id, portfolio_id=portfolio.id
        ).first()
        assert apple_portfolio_investment is not None
        apple_initial_amount = apple_portfolio_investment.amount
        apple_initial_share = apple_portfolio_investment.share

        invest_amount_in_portfolio(target_investment.id, portfolio.id, 1000)

        portfolio = Portfolio.query.first()
        assert portfolio.amount == initial_amount + 1000

        apple_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=target_investment.id, portfolio_id=portfolio.id
        ).first()
        assert apple_portfolio_investment.amount == apple_initial_amount + 1000
        assert apple_portfolio_investment.share == (apple_initial_amount + 1000) / (
            initial_amount + 1000
        )
        assert apple_initial_share != apple_portfolio_investment.share


@pytest.mark.unit
def test_deposit_investment_into_new_investment(client):
    from app import db
    from app.business_logic.portfolio import invest_amount_in_portfolio
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    with client.application.app_context():
        portfolio = Portfolio.query.first()  # is a CTO
        assert portfolio is not None
        initial_amount = portfolio.amount

        # we create a new investment with label "Spotify Inc."
        new_investment = Investment(
            type="stock",
            isin="US85333R1023",
            label="Spotify Inc.",
            price=150.0,
            srri=5,
        )
        db.session.add(new_investment)

        # we know customer has allready invested in "Apple Inc."
        apple_investment = Investment.query.filter_by(label="Apple Inc.").first()
        apple_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=apple_investment.id, portfolio_id=portfolio.id
        ).first()
        assert apple_portfolio_investment is not None
        apple_initial_amount = apple_portfolio_investment.amount
        apple_initial_share = apple_portfolio_investment.share

        invest_amount_in_portfolio(new_investment.id, portfolio.id, 2000)

        portfolio = Portfolio.query.first()
        assert portfolio.amount == initial_amount + 2000

        apple_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=apple_investment.id, portfolio_id=portfolio.id
        ).first()
        assert apple_portfolio_investment.amount == apple_initial_amount
        assert apple_initial_share != apple_portfolio_investment.share

        new_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=new_investment.id, portfolio_id=portfolio.id
        ).first()
        assert new_portfolio_investment is not None
        assert new_portfolio_investment.amount == 2000
        assert new_portfolio_investment.share == 2000 / (initial_amount + 2000)


@pytest.mark.unit
def test_deposit_investment_invalid_investment_id(client):
    response = client.post(
        f"/portfolios/deposit/1",  # portfolio 1 exists and is a CTO
        json={"amount": 1000, "investment_id": 999999},
    )
    assert response.status_code == 404
    assert b"Not Found" in response.data


@pytest.mark.unit
def test_deposit_investment_valid_investment_id(client):
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio

    with client.application.app_context():
        portfolio = Portfolio.query.first()  # is a CTO
        target_investment = Investment.query.filter_by(label="Apple Inc.").first()
        assert target_investment is not None

        response = client.post(
            f"/portfolios/deposit/{portfolio.id}",
            json={"amount": 1000, "investment_id": target_investment.id},
        )
        assert response.status_code == 200
        assert b"Investment deposited successfully" in response.data


@pytest.mark.unit
def test_deposit_investment_invalid_portfolio_type(client):
    from app.models.portfolio import Portfolio
    from app.models.investment import Investment
    from app import db

    with client.application.app_context():
        portfolio = Portfolio.query.first()
        assert portfolio is not None
        portfolio.type = "INVALID_TYPE"  # we manually set an invalid type
        db.session.commit()

        target_investment = Investment.query.filter_by(label="Apple Inc.").first()
        assert target_investment is not None

        response = client.post(
            f"/portfolios/deposit/{portfolio.id}",
            json={"amount": 1000, "investment_id": target_investment.id},
        )
        assert response.status_code == 400
        assert b"Invalid portfolio type" in response.data


@pytest.mark.unit
def test_withdraw_investment_successfully(client):
    from app.business_logic.portfolio import withdraw_amount_from_portfolio
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    with client.application.app_context():
        portfolio = Portfolio.query.first()
        assert portfolio is not None
        initial_amount = portfolio.amount

        # we want to withraw in investment labelled "Apple Inc."
        target_investment = Investment.query.filter_by(label="Apple Inc.").first()
        apple_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=target_investment.id, portfolio_id=portfolio.id
        ).first()
        assert apple_portfolio_investment is not None
        apple_initial_amount = apple_portfolio_investment.amount
        apple_initial_share = apple_portfolio_investment.share

        withdraw_amount_from_portfolio(target_investment.id, portfolio.id, 1000)

        portfolio = Portfolio.query.first()
        assert portfolio.amount == initial_amount - 1000
        apple_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=target_investment.id, portfolio_id=portfolio.id
        ).first()
        assert apple_portfolio_investment.amount == apple_initial_amount - 1000
        assert apple_initial_share != apple_portfolio_investment.share


@pytest.mark.unit
def test_not_enough_amount_to_withdraw(client):
    from app.business_logic.portfolio import withdraw_amount_from_portfolio
    from app.models.investment import Investment
    from app.models.portfolio import Portfolio
    from app.models.portfolio_investment import PortfolioInvestment

    with client.application.app_context():
        portfolio = Portfolio.query.first()
        assert portfolio is not None

        # we want to withraw in investment labelled "Apple Inc."
        target_investment = Investment.query.filter_by(label="Apple Inc.").first()
        apple_portfolio_investment = PortfolioInvestment.query.filter_by(
            investment_id=target_investment.id, portfolio_id=portfolio.id
        ).first()

        # try to withdraw more than the amount available
        with pytest.raises(ValueError, match="Not enough amount to withdraw"):
            withdraw_amount_from_portfolio(
                target_investment.id,
                portfolio.id,
                apple_portfolio_investment.amount + 1,
            )


@pytest.mark.unit
def test_withdraw_investment_invalid_amount(client):
    response = client.post(
        f"/portfolios/withdraw/1",  # portfolio 1 exists and is a CTO
        json={"amount": 1000000, "investment_id": 1},
    )
    assert response.status_code == 400
