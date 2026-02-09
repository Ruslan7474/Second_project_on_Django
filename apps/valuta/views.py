from django.shortcuts import render
from apps.valuta.currency import get_rates

def valuta_page(request):
    rates = get_rates()

    context = {
        "usd": rates["USD"],
        "eur": rates["EUR"],
        "rub": rates["RUB"],
        "kzt": rates["KZT"],
    }
    return render(request, "page/valuta.html", context)