import csv

def get_by_date(date="2017-08-08", name="PCLN", filename='20170808PCLN.csv'):
    """Функция ищет  date, name линейным поиском , не потребляет памяти  """
    vvod_date = input('Дата в формате yyyy-mm-dd [all]:')
    if vvod_date != '' : date = vvod_date
    vvod_name = input('Тикер [all]:')
    if vvod_name != '': name = vvod_name
    vvod_file = input('Файл [dump.csv]:')
    if vvod_file != '': filename = vvod_file
    with open(f'data/result6.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(f'data/{filename}', 'w+') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=['date', 'open', 'high', 'low', 'close', 'volume', 'Name'])
            writer.writeheader()
            for row in reader:
                if row['date'] == date and row ['Name'] == name:
                    writer.writerow(row)

