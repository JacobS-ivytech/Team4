from .models import Cart


def cart(request):
    if request.user.is_authenticated:
        return {"cart": Cart.get_for_user(request.user)}
    return {}
