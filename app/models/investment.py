from app import db


class Investment(db.Model):
    __tablename__ = "investment"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    isin = db.Column(db.String(20), unique=True)
    label = db.Column(db.String(100))
    price = db.Column(db.Float)
    srri = db.Column(db.Integer)

    portfolio_investments = db.relationship(
        "PortfolioInvestment",
        back_populates="investment",
        cascade="all, delete-orphan",
    )

    portfolios = db.relationship(
        "Portfolio",
        secondary="portfolio_investment",
        back_populates="investments",
        viewonly=True,
    )
