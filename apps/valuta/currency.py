import requests
import xml.etree.ElementTree as ET


URL = "https://www.nbkr.kg/XML/daily.xml"


def get_rates():
    response = requests.get(URL, timeout=10)
    response.encoding = "utf-8"

    tree = ET.fromstring(response.text)


    currencies = {
        "USD": None,
        "EUR": None,
        "RUB": None,
        "KZT": None,
    }


    for currency in tree.findall("Currency"):
        code = currency.get("ISOCode")
        if code in currencies:
            value = currency.find
            currencies(code) = float(value.replace(',','.'))

        return currencies