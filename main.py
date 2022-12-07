from sorter import select_sorted
from get_date import get_by_date

if __name__ == '__main__':
    select_sorted(sort_columns=['high'], limit=50, filename='dump.csv')
    get_by_date(date="2017-08-08", name="PCLN", filename='20170808PCLN.csv')
