from app import db


class PortfolioInvestment(db.Model):
    __tablename__ = "portfolio_investment"

    # Composite primary key enforcing uniqueness
    # between portfolio_id and investment_id
    portfolio_id = db.Column(
        db.Integer, db.ForeignKey("portfolio.id"), primary_key=True
    )
    investment_id = db.Column(
        db.Integer, db.ForeignKey("investment.id"), primary_key=True
    )

    amount = db.Column(db.Float, nullable=False)
    share = db.Column(db.Float, nullable=False)

    portfolio = db.relationship("Portfolio", back_populates="portfolio_investments")
    investment = db.relationship("Investment", back_populates="portfolio_investments")
