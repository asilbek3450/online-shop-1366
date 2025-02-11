from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, ProductCategory
from django.shortcuts import get_object_or_404

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
        eng_qimmatlari = Product.objects.order_by('-price')[:8]
        context = {
            'products': products,
            'categories': categories,
            'new_products': new_products,
            'eng_qimmatlari': eng_qimmatlari
        }
        return context
        

def StorePage(request, c):
    products = Product.objects.filter(category__name=c)
    categories = ProductCategory.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, 'store.html', context)


def ProductPage(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = ProductCategory.objects.all()

    context = {
        'product': product,
        'categories': categories
    }

    return render(request, 'product.html', context)