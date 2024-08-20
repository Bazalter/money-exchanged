import requests


response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
data = response.json()
valutes = data.get('Valute')
soarted_valutes = sorted(valutes.items(), key=lambda item: item[1]['Value'])
for name, char in soarted_valutes:
    print(f'{name}, полное наименование {char["Name"]} значение {char["Value"]}')



# if __name__ == "__main__":
#     print(valutes)
