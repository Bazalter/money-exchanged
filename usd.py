import requests


# response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
# data = response.json()
# valutes = data.get('Valute')
# for name, char in valutes.items():
#     if char['Nominal'] != 1:
#         char['Value'] /= char['Nominal']
#         char['Previous'] /= char['Nominal']
#         char['Nominal'] = 1
# print(valutes)
# soarted_valutes = sorted(valutes.items(), key=lambda item: item[1]['Value'])
# for name, char in soarted_valutes:
#     print(f'{name}, полное наименование {char["Name"]} значение {char["Value"]}')


class Valutes:
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    valutes = data.get('Valute')
    _adjusted = False

    def __init__(self, value: int | float, currency: str, curr_changed: str):
        if not Valutes._adjusted:
            Valutes.adjust_values()
            Valutes._adjusted = True

        self.value = value
        self.currency = currency
        self.curr_changed = curr_changed

        if currency not in self.valutes and currency != "RUB":
            raise ValueError("Invalid currnecy")

        if curr_changed not in self.valutes and curr_changed != "RUB":
            raise ValueError("Invalid currnecy")

    @classmethod
    def adjust_values(cls):
        """Корректирует значения Value и Previous на основе Nominal для всех валют."""
        for name, char in cls.valutes.items():
            if char['Nominal'] != 1:
                char['Value'] /= char['Nominal']
                char['Previous'] /= char['Nominal']
                char['Nominal'] = 1

    @classmethod
    def get_values(cls):
        """Возвращает обработанные данные."""
        return cls.valutes

    @classmethod
    def list_currency(cls):
        """ Возвращает список валют и их значение"""
        soarted_valutes = sorted(cls.valutes.items(), key=lambda item: item[1]['Value'])
        result = []
        for name, char in soarted_valutes:
            # result.append({
            #     'codename': name,
            #     'name': char["Name"],
            #     "value": char["Value"]
        #     })
        # return result
            result.append(f'{name}, Полное наименование {char["Name"]} значение {char["Value"]}')
        return "\n".join(result)

    def calc_salary(self):

        if self.currency == "RUB":
            salary = self.value / self.__class__.valutes[self.curr_changed]["Value"]
            print(self.valutes[self.curr_changed]["Value"])
            return salary

        calc_valutes = self.__class__.valutes[self.currency]['Value']
        salary = calc_valutes * self.value / self.__class__.valutes[self.curr_changed]["Value"]
        return salary


if __name__ == "__main__":

    a = Valutes(80000, 'EUR', 'KZT')
    print(a.calc_salary())
    # print(Valutes.list_currency())
    # print(a.__class__.get_values())