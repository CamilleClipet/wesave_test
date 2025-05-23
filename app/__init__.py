from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.controllers.portfolio_controller import portfolio_bp

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(portfolio_bp)

    with app.app_context():
        from app.models.investment import Investment
        from app.models.portfolio import Portfolio
        from app.models.portfolio_investment import PortfolioInvestment

        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
