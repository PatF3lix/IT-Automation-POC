from flask import Flask

from .routes.ui_routes import ui_bp
from .routes.employee_routes import employee_bp
from .routes.ticket_routes import ticket_bp
from .routes.asset_routes import asset_bp
from .routes.onboarding_routes import onboarding_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(ui_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(asset_bp)
    app.register_blueprint(onboarding_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)