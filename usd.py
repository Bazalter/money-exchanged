import requests


response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
data = response.json()

valutes = data['Valute']['USD']['Value']
# for a in valutes.items():
#     print(a)
# soarted_valutes = sorted(valutes.items, key=lambda item: item[1]['Value'])


if __name__ == "__main__":
    print(valutes)
