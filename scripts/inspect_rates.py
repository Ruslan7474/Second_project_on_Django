import requests
import xml.etree.ElementTree as ET

URL='https://www.nbkr.kg/XML/daily.xml'

r = requests.get(URL, timeout=10)
print('HTTP', r.status_code)
root = ET.fromstring(r.text)
for i, c in enumerate(root.findall('.//Currency'), start=1):
    code = c.get('ISOCode') or c.get('ISO') or c.get('Code')
    char = c.findtext('CharCode')
    val = c.find('Value')
    name = c.findtext('CurrencyName')
    print(i, 'code_attr:', code, 'char:', char, 'value:', (val.text if val is not None else None), 'name:', name)
