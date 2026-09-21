from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Cart, CartItem, Category, MenuItem


def index(request):
    return render(request, "home.html")


def menu(request):
    categories = Category.objects.prefetch_related("items").all()
    return render(request, "menu.html", {"categories": categories})


def menu_item_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, "menu_item_detail.html", {"item": item})


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    cart = Cart.get_for_user(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("cart")


class CustomLoginView(LoginView):
    template_name = "login.html"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def cart(request):
    cart = Cart.get_for_user(request.user)
    return render(request, "cart.html", {"cart": cart})


@login_required
@require_POST
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user=request.user)
    quantity = int(request.POST.get("quantity", cart_item.quantity))
    if quantity < 1:
        cart_item.delete()
    else:
        cart_item.quantity = min(quantity, 20)
        cart_item.save()
    return redirect("cart")


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("cart")


@login_required
def clear_cart(request):
    cart = Cart.get_for_user(request.user)
    cart.cartitem_set.all().delete()
    return redirect("cart")
