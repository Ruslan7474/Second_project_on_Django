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


    for currency in tree.findall('.//Currency'):
        code = currency.get('ISOCode') or currency.get('ISO') or currency.get('Code')
        if code in currencies:
            value_elem = currency.find('Value')
            if value_elem is None or not value_elem.text:
                continue
            try:
                currencies[code] = float(value_elem.text.replace(',', '.'))
            except ValueError:
                continue

    return currencies