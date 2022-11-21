import os, csv
from prettytable import PrettyTable, SINGLE_BORDER
from datetime import datetime
from expense import Expense

class Table:
    pass

    file_path = ''
    file_name = '\\data.csv'

    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as file:
            file_path = file.readline().strip()
            file_name = file.readline().strip()
            
    def set_file_name(new_name:str):
        Table.file_name = '\\'+new_name+'.csv'
        Table.replase_row_in_file(1, 'data.txt', Table.file_name)
        
    def set_file_path(new_path:str):
        Table.file_path = new_path
        Table.replase_row_in_file(0, 'data.txt', new_path)
        
    def replase_row_in_file(row_count:int, file_p:str, new_data:str):
        with open(file_p, 'r') as file:
            old_file = file.readlines()
        old_file[row_count] =  new_data+'\n'
        with open(file_p, 'w') as file:
            file.writelines(old_file)

    def table_from_database(sort_key:str = None,
                            revers = False,
                            range_start = None,
                            range_end = None,
                            types = None,
                            colomns_to_print:list = ["Дата", "Ціна", "Назва"],
                            for_telegram = True):
        
        path = Table.file_path + Table.file_name
        table = PrettyTable(field_names=colomns_to_print) # Створення таблиці
        stats = {'cost_sum':0, # Підготовка саттистики
                'date_start':None,
                'date_end':None,
                'bigest_expanse':0,
                'bigest_expanse_name':'',
                'bigest_expanse_date':'',
                'Average_day_cost':0,
                'days':None}
        
        ##########  ПІДГОТОВКА ПЕРЕВІРОК  ##########
        type_check = True
        date_check = True
        for_once = True
        
        if range_start != None:
            range_start_d = datetime.strptime(range_start, Expense.format_date)
            if range_end != None:
                range_end_d = datetime.strptime(range_end, Expense.format_date)
            else:
                range_end_d = range_start_d
        ##########  КІНЕЛЬ ПІДГОТОВКИ ПЕРЕВІРОК  ##########
        
        ##########  ФОРМУВАННЯ ТАБЛИЦІ  ##########  
        with open(path, 'r') as file: 
            reader = csv.DictReader(file, delimiter=';', fieldnames=["Дата", "Ціна", "Назва", "Тип"])
            for line in reader:
                ##########  ПЕРЕВІРКА  ##########
                if types != None:
                    type_check = line["Тип"] in types
                    
                line_date = datetime.strptime(line["Дата"], Expense.format_date)
                if range_start != None:
                    date_check = line_date >= range_start_d and line_date <= range_end_d
                ##########  КІНЕЛЬ ПЕРЕВІРКИ  ##########
                
                new_line = []
                if type_check and date_check:
                    ##########  РОЗРАХУНОК СТАТИСТИКИ  ##########
                    line["Ціна"] = int(line["Ціна"])
                    stats['cost_sum']+=line["Ціна"]
                    if for_once:
                        stats['date_end'] = line_date
                        stats['date_start'] = line_date
                        for_once = False
                    if stats['bigest_expanse'] < line["Ціна"]:
                        stats['bigest_expanse'] = line["Ціна"]
                        stats['bigest_expanse_name'] = line["Назва"]
                        stats['bigest_expanse_date'] = line["Дата"]
                    if line_date > stats['date_end']: stats['date_end'] = line_date
                    if line_date < stats['date_start']: stats['date_start'] = line_date
                    ##########  КІНЕЦЬ РОЗРАХУНКУ СТАТИСТИКИ  ##########
                    
                    if "Дата" in colomns_to_print and for_telegram: # Зменшення розміру дати для телеграму
                        line['Дата'] = datetime.strftime(line_date, '%d.%m')
                    
                    for i in colomns_to_print:
                        new_line.append(line[i])
                        
                    table.add_row(new_line)
        
        ##########  СОРТУВАННЯ ТА ОФОРМЛЕННЯ  ##########
        table.set_style(SINGLE_BORDER)
        if sort_key != None:
            try: 
                table.sortby = sort_key    
            except:
                print('Спроба сортування за стовбцем, якого не існує')
        table.reversesort = revers
        stats['days'] = stats['date_end'] - stats['date_start'] 
        stats['Average_day_cost'] = stats['cost_sum'] / (stats['days'].days+1)
        if 'Назва' in colomns_to_print:
            table.align["Назва"] = 'l'
        if 'Ціна' in colomns_to_print:
            table.align["Ціна"] = 'l'
        
        if for_telegram:
            telegram_table = ''
            split_table = str(table).split('\n')
            for line in split_table:
                telegram_table += ('<code>' + line + '</code>' + '\n')
            telegram_table += f'\nВиведено дати з {datetime.strftime(stats["date_start"], Expense.format_date)} до {datetime.strftime(stats["date_end"], Expense.format_date)}. Це {stats["days"].days+1} днів.\n\nЗа цей проміжок витрачено {stats["cost_sum"]} грн. Це у середньому {round(stats["Average_day_cost"])} грн. {round((stats["Average_day_cost"]%1)*100)} к. на день.\n\nА найбільша витрата була зроблена {stats["bigest_expanse_date"]}, і це "{stats["bigest_expanse_name"]}", що коштувало {stats["bigest_expanse"]} грн.\n'
            return telegram_table
        else:
            return str(table)+f'\nВиведено дати з {datetime.strftime(stats["date_start"], Expense.format_date)} до {datetime.strftime(stats["date_end"], Expense.format_date)}. Це {stats["days"].days+1} днів.\n\nЗа цей проміжок витрачено {stats["cost_sum"]} грн. Це у середньому {round(stats["Average_day_cost"])} грн. {round((stats["Average_day_cost"]%1)*100)} к. на день.\n\nА найбільша витрата була зроблена {stats["bigest_expanse_date"]}, і це "{stats["bigest_expanse_name"]}", що коштувало {stats["bigest_expanse"]} грн.\n'
                

    def append_file(name, cost, date=None, type=None):

        path = Table.file_path+Table.file_name
        new_row = Expense(name=name, cost=cost, date=date, type=type)
        with open(path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(new_row.list())