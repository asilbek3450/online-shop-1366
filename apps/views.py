from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, ProductCategory

# Create your views here.
# Function based view
def base_page(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    new_products = Product.objects.order_by('-id')[:5]
    context = {
        'products': products,
        'categories': categories,
        'new_products': new_products
    }
    return render(request, 'base.html', context)


# Class based view
class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        products = Product.objects.all()
        categories = ProductCategory.objects.all()
        new_products = Product.objects.order_by('-id')[:5]
        context = {
            'products': products,
            'categories': categories,
            'new_products': new_products
        }
        return context
        
    