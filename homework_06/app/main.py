import os
from flask import Flask
from flask_migrate import Migrate
from flask import render_template
from app.views.products import products_app
from .moduls.moduls import db
app = Flask(__name__)
app.register_blueprint(products_app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI",
    "sqlite:///test.db",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", endpoint="index")
def hello():
    return render_template(
        "index.html"
    )


@app.route("/hello/<name>/")
def hello_name(name):
    name=name.strip()
    return render_template(
        "hello.html",
        name=name,
    )




if __name__ =="__main__":
    app.run(debug=True)