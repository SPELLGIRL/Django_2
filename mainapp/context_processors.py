from django.http import HttpRequest
from basketapp.models import Basket
from .models import MainMenu


def main_menu(request: HttpRequest):
    if request.user.is_authenticated:
        load_basket = Basket.objects.filter(user=request.user)
    else:
        load_basket = None

    return {
        'basket': load_basket,
        'main_menu_links': MainMenu.objects.all()
    }
