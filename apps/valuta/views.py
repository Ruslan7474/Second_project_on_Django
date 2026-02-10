from django.shortcuts import render
from apps.valuta.currency import get_rates

def valuta_page(request):
    rates = get_rates()

    rates = {**rates, "KGS": 1.0}

    amount = request.GET.get("amount")
    from_code = request.GET.get("from")
    to_code = request.GET.get("to")
    result = None
    error = None

    if amount and from_code and to_code:
        try:
            amount_val = float(str(amount).replace(",", "."))
            from_rate = rates.get(from_code)
            to_rate = rates.get(to_code)
            if from_rate is None or to_rate is None:
                error = "Нет курса для выбранной валюты."
            else:
                result = round((amount_val * from_rate) / to_rate, 4)
        except ValueError:
            error = "Неверное число в поле суммы."

    context = {
        "usd": rates["USD"],
        "eur": rates["EUR"],
        "rub": rates["RUB"],
        "kzt": rates["KZT"],
        "amount": amount,
        "from_code": from_code,
        "to_code": to_code,
        "result": result,
        "error": error,
    }
    return render(request, "page/valuta.html", context)
