from typing import Any
from django.views.generic import TemplateView
from store_app.models import Product

class ProductsIndexView(TemplateView):
    template_name="store_app/products_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            products=Product.objects.all(),
        )
        return context