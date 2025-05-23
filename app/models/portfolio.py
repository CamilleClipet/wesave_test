from app import db


class Portfolio(db.Model):
    __tablename__ = "portfolio"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    portfolio_investments = db.relationship(
        "PortfolioInvestment",
        back_populates="portfolio",
        cascade="all, delete-orphan",
    )

    investments = db.relationship(
        "Investment",
        secondary="portfolio_investment",
        back_populates="portfolios",
        viewonly=True,
    )
