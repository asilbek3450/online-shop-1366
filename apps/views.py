from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Foydalanuvchining savatini olish yoki yaratish
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Mahsulotni savatga qo'shish
    cart.add_product(product)  # Bu yerda add_product metodi ishlatiladi
    
    return redirect('cart_detail')  # Foydalanuvchini savat sahifasiga yo'naltirish


def base_page(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    new_products = Product.objects.order_by('-id')[:5]

    # Foydalanuvchining savatini olish
    cart_products = Cart.objects.filter(user=request.user).first()
    cart_items = cart_products.items.all() if cart_products else []

    context = {
        'products': products,
        'categories': categories,
        'new_products': new_products,
        'cart_products': cart_items  # Savatdagi mahsulotlar
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
    # Kategoriya nomiga mos mahsulotlarni filtrlash
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


@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()  # Foydalanuvchining savatini olish
    if not cart:
        return render(request, 'cart.html', {'error': 'Savatda mahsulotlar mavjud emas'})
    
    cart_items = cart.items.all()  # Savatdagi mahsulotlar
    total_price = cart.get_total_price()  # Savatdagi jami narx

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


# Savatdagi mahsulotni olib tashlash uchun view
@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        cart.remove_product(product)
    
    return redirect('cart_detail')


# Foydalanuvchini tizimga kirish
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cart_detail')  # Tizimga kirgandan keyin savatga o'tish
            else:
                messages.error(request, "Foydalanuvchi topilmadi yoki parol noto'g'ri.")
        else:
            messages.error(request, "Formada xatolik mavjud.")
    else:
        form = AuthenticationForm()

    return render(request, '404.html', {'form': form})

# Foydalanuvchini ro'yxatdan o'tkazish
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cart_detail')  # Ro'yxatdan o'tganidan keyin savatga o'tish
        else:
            messages.error(request, "Ro'yxatdan o'tishda xatolik.")
    else:
        form = UserCreationForm()

    return render(request, '404.html', {'form': form})

# Tizimdan chiqish
def logout_view(request):
    logout(request)
    return redirect('login')


