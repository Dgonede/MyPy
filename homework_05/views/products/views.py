from flask import Blueprint
from flask import render_template
from .crud import storage
from werkzeug.exceptions import NotFound


products_app = Blueprint(
    "products_app",
    __name__,
    url_prefix="/products",
)

@products_app.route("/", endpoint="index")
def get_product_list():
    return render_template(
        "products/index.html",
        products=storage.get(),
        )


@products_app.route("/<int:product_id>/", endpoint="details")
def get_products_by_id(product_id):
    product = storage.get_by_id(product_id)
    if not product:
        raise NotFound(f"product # {product_id} not found")
    return render_template(
        "products/details.html",
        product=product,
        )

