import datetime

class Expense:
    """Клас для позиції витрати
    
    Виводиться строкою:
    Дата: {date}, Ціна: {cost}, Назва: {name}
    """
    format_date = '%d.%m.%Y'
    default_name = 'Без назви'
    default_cost = 0.0
    default_date = datetime.datetime.now()
    default_type = 'Різне'
    
    def __init__(self, name:str=None, cost:float=0.0, date:str=None, type:str=None) -> None:
        """Створення об'єкта, на який витратили гроші
        Args:
            name (str, optional): Назва позиції.Якщо не вказано: Без назви\n
            cost (float, optional): Ціна. Якщо не вказано: 0\n
            date (str, optional): Дата: <день.місяць.рік>. Якщо не вказано: сьогодні.\n
            type (str, optional): Тип Позиції. Якщо не вказано: Різнеfdf
        """
        if date != None and date != '':
            try: self.__date = datetime.datetime.strptime(date, '%d.%m.%y')
            except: 
                try: self.__date = datetime.datetime.strptime(date, Expense.format_date)
                except:
                    try: self.__date = datetime.datetime.strptime(date, '%y.%m.%d')
                    except Exception: self.__date = datetime.datetime.strptime(date, '%Y.%m.%d')
        else: self.__date = Expense.default_date

        if cost < 0: self.__cost = Expense.default_cost
        else: self.__cost = cost

        if name == None or name == '': self.__name = Expense.default_name
        else: self.__name = name
        
        if type == None or type == '': self.__type = Expense.default_type
        else: self.__type = type

    @property
    def date(self)->str:
        """Дата витрати

            date (str): Дата: <день.місяць.рік>
        """
        return datetime.datetime.strftime(self.__date, Expense.format_date)
    @date.setter
    def date(self, date:str):
        if date != '':
            try: self.__date = datetime.datetime.strptime(date, '%d.%m.%y')
            except: 
                try: self.__date = datetime.datetime.strptime(date, Expense.format_date)
                except:
                    try: self.__date = datetime.datetime.strptime(date, '%y.%m.%d')
                    except: self.__date = datetime.datetime.strptime(date, '%Y.%m.%d')

        
    @property
    def name(self)->str:
        """Назва витрати
        
            name (str): Назва
        """
        return self.__name
    @name.setter
    def name(self, name:str): self.__name = name
    
    @property
    def cost(self)->float:
        """Вартість витрати

            float: Число не меньше нуля
        """
        return self.__cost
    @cost.setter
    def cost(self, cost:float):
        if cost < 0: self.__cost=0
        else: self.__cost = cost
    
    @property
    def type(self)->str:
        """Тип витрати

            str: Назва типу
        """
        return self.__type
    @type.setter
    def type(self, type:str):
        if type == '': self.__type = Expense.default_type
        else: self.__type = type
    
    def list(self)->list: return [self.date, str(self.__cost), self.__name, self.__type]
    
    def __str__(self) -> str: return f"Дата: {self.date},\tЦiна: {self.__cost},\tНазва: {self.__name},\tТип: {self.__type}"
    
    def __int__(self) -> int: return int(self.__cost)