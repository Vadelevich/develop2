import csv
import os

choice = {
    '1': 'open',
    '2': 'close',
    '3': 'high',
    '4': 'low',
    '5': 'volume'
}


def write_limit_to_end_rezalt(limit, filename, counter_file):
    file_last_result = open(f'data/result{counter_file - 1}.csv')
    reader_last_result = csv.DictReader(file_last_result)
    counter_line = limit
    with open(f'{filename}', 'a') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['date', 'open', 'high', 'low', 'close', 'volume', 'Name'])
        writer.writeheader()
        for row in reader_last_result:
            if counter_line != 0:
                writer.writerow(row)
                counter_line -= 1
            else:
                break


def write_all_to_file(iterator_pointer, result_file):
    for row in iterator_pointer:
        result_file.writerow(row)


def concatenate_files(count_file, sort_key):
    print('#' * 50)
    for i in range(count_file - 1):

        file_i = open(f'data/{i + 1}.csv')

        reader_i = csv.DictReader(file_i)

        result_file = open(f'data/result{i + 1}.csv', 'w')
        result_writer = csv.DictWriter(result_file, [*reader_i.fieldnames])
        result_writer.writeheader()

        if i == 0:
            print('-- write first file to result files')
            write_all_to_file(reader_i, result_writer)
        else:
            print(f'-- write {i + 1} file to prev result')
            file_prev = open(f'data/result{i}.csv')
            prev_reader = csv.DictReader(file_prev)

            row_i = reader_i.__next__()
            prev_file_row = prev_reader.__next__()

            while True:
                try:
                    var_1 = float(row_i[sort_key])
                    var_2 = float(prev_file_row[sort_key])
                except:
                    var_1 = row_i[sort_key]
                    var_2 = prev_file_row[sort_key]
                if var_1 > var_2:
                    result_writer.writerow(prev_file_row)
                    try:
                        prev_file_row = prev_reader.__next__()
                    except:
                        write_all_to_file(reader_i, result_writer)
                        break

                else:
                    result_writer.writerow(row_i)
                    try:
                        row_i = reader_i.__next__()
                    except:
                        write_all_to_file(prev_reader, result_writer)
                        break

            file_prev.close()

        result_file.close()
        file_i.close()


def create_temp_folder():
    """Функция создает пустую папку"""
    try:
        os.mkdir('data')
    except FileExistsError:
        print('-- folder already ready')


def write_to_tmp_csv(sort_tmp_list, conter_file):
    """Функция записывает данные во временый файл """
    with open(f'data/{conter_file}.csv', mode='a') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['date', 'open', 'high', 'low', 'close', 'volume', 'Name'])
        writer.writeheader()
        writer.writerows(sort_tmp_list)


def select_sorted(sort_columns=['high'], limit=50, filename='dump.csv', ):
    vvod = input('Сортировать по цене открытия (1),закрытия (2),максимум [3],минимум (4),объем (5)')
    if vvod != '': sort_columns = [choice[vvod]]
    vvod_limit = input('Ограничение выборки [10]: ')
    if vvod_limit != '': limit = vvod_limit
    vvod_file = input('Название файла для сохранения результата [dump.csv]:')
    if vvod_file != '': filename = vvod_file

    with open('all.csv', 'r') as csv_file:
        sort_key = sort_columns[0]
        counter_row = 0
        tmp_list = []
        create_temp_folder()
        counter_file = 1
        for row in csv.DictReader(csv_file):
            counter_row += 1
            tmp_list.append(row)
            if counter_row > 100000:
                counter_row = 0
                newlist = sorted(tmp_list, key=lambda d: d[sort_columns[0]])
                write_to_tmp_csv(newlist, counter_file)
                counter_file += 1
                tmp_list = []
        if len(tmp_list) > 0:  #
            write_to_tmp_csv(tmp_list, counter_file)
    concatenate_files(counter_file, sort_key)
    write_limit_to_end_rezalt(limit, filename, counter_file)

    return counter_file
