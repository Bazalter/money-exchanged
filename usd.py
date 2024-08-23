import requests


# response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
# data = response.json()
# valutes = data.get('Valute')
# print(valutes)
# soarted_valutes = sorted(valutes.items(), key=lambda item: item[1]['Value'])
# for name, char in soarted_valutes:
#     print(f'{name}, полное наименование {char["Name"]} значение {char["Value"]}')


class Valutes:
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    valutes = data.get('Valute')

    def __init__(self, value: int | float, currency: str, curr_changed: str = "USD"):
        self.value = value
        self.currency = currency
        self.curr_changed = curr_changed

        if currency not in self.valutes and currency != "RUB":
            raise ValueError("Invalid currnecy")

        if curr_changed not in self.valutes and curr_changed != "RUB":
            raise ValueError("Invalid currnecy")

    @classmethod
    def list_currency(cls):
        soarted_valutes = sorted(cls.valutes.items(), key=lambda item: item[1]['Value'])
        for name, char in soarted_valutes:
            print(f'{name}, Полное наименование {char["Name"]} значение {char["Value"]}')

    def calc_salary(self):

        if self.currency == "RUB":
            salary = self.value / self.valutes[self.curr_changed]["Value"]
            return f' Your salary {salary} чертовых зеленых бумажек'

        calc_valutes = self.valutes[self.currency]['Value']
        salary = calc_valutes * self.value / self.valutes[self.curr_changed]["Value"]
        return f' Your salary {salary} чертовых бумажек {self.valutes[self.curr_changed]["Name"]}'


if __name__ == "__main__":

    a = Valutes(10000, 'RUB')
    print(a.calc_salary())
