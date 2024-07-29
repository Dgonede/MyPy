from flask import Flask
from flask import render_template
from views.products import products_app

app = Flask(__name__)
app.register_blueprint(products_app)

@app.route("/")
def hello():
    return "<h1>Hello World</h1>"


@app.route("/hello/<name>/")
def hello_name(name):
    name=name.strip()
    return render_template(
        "index.html",
        name=name,
    )




if __name__ =="__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)