import os
from flask import Flask, url_for
from flask_migrate import Migrate
from src.config import configs
from src.utils.db import db
from src.utils.blueprints import bp
import urllib.parse as up
from flask_script import Manager
from flask_jwt_extended import JWTManager

app = Flask(__name__)
config = os.environ.get('PYTH_SRVR', 'default')
config = configs.get(config)
app.config.from_object(config)
app.register_blueprint(bp)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
manager = Manager(app)


@manager.command
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = up.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == "__main__":
    manager.run()
