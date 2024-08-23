from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (
    TemplateView, 
    CreateView, 
    ListView,
    DetailView,
    UpdateView,
)
from store_app.models import Product, Order
from celery.result import AsyncResult 
from .forms import CategoryCreateUpdateForm
from .models import Category
from .mixins import PageTitleMixin


class ProductsIndexView(TemplateView):
    template_name="store_app/products_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            products=(
                Product.objects
                .filter(archived=False)
                .select_related("category")
                .all()
        ),
            )
        return context
    

class OrdersIndexView(TemplateView):
    template_name = "store_app/orders_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            # orders=Order.objects.prefetch_related("products").all(),
            orders=(
                Order.objects
                .select_related("user")
                .prefetch_related("order_products__product")
                .all()
            ),
        )
        return context
    

def task_status(request: HttpRequest) -> HttpResponse:
    context = {}
    task_id = request.GET.get("task_id")
    # result = AsyncResult(id=task_id) 
    # is_ready = result.ready()
    # status = result.status
    # task_result = result.result
    context.update(
        task_id=task_id,
        is_ready="is_ready",
        status="status",
        result="task_result",
    )
    return render(
        request=request,
        template_name="store_app/task_status.html",
        context=context,
    ) 


def create_category(request):
    if request.method == 'POST':
        print('processing')
    
        form = CategoryCreateUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            print('is valid')
            form.save()
            return HttpResponseRedirect('/')
        else:
            print('errors')
    else:
        form = CategoryCreateUpdateForm()            
    context = {
        'create_form': form,
    }
    return render(request, 'store_app/create_category.html', context)


class CreateCategory(PageTitleMixin, CreateView):
    model = Category
    form_class = CategoryCreateUpdateForm
    success_url = '/'
    page_title = 'Category create'
   
    
class ListCategory(PageTitleMixin, ListView):
        model = Category
        page_title = 'List category'
        paginate_by = 3


class UpdateCategory(PageTitleMixin, UpdateView):
        model = Category
        form_class = CategoryCreateUpdateForm
        page_title = 'Category update'
        success_url = '/'
       


class ReadCategory(PageTitleMixin, DetailView):
        model = Category
        page_title = 'Category update'
                      