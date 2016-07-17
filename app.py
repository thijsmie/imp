from flask import Flask
import models
import routers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
models.db.init_app(app)

app.register_blueprint(routers.ProductRouter, url_prefix="/product")
app.register_blueprint(routers.StockRouter, url_prefix="/stock")

app.run();