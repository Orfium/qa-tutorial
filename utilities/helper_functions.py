from datetime import datetime


def convert_str_to_date_obj(list_of_strings: list, date_format: str) -> list:
    """
    Convert a list of strings to datetime objects
    :param list_of_strings: A list with the dates in strings (it can be only one date)
    :param date_format: specify the format of the dates, example '%d/%m/%Y' or '%d-%m-%Y'
    :return: A list with date objects
    """
    return [datetime.strptime(s, date_format) for s in list_of_strings]


def convert_str_to_number(item_list: list):
    try:
        item_list = [float(s.replace(',', '')) if type(s) == str else s for s in item_list]
    except ValueError:
        print("The list doesn't contain numbers")
    return item_list


def is_sorted(item_list: list):
    return all(item_list[i] >= item_list[i+1] for i in range(len(item_list)-1))

# USE FUNCTION get_all_strings_by_column_name(self, column_name) from Driver.py
# def get_all_items_of_column(obj, column_locator):
#     """Call it with the 'self' as first argument
#     Example: get_all_items_of_column(self, (By.XPATH, '//td[3]')
#     """
#     elements = obj.findElements(*column_locator)
#     items_list = [element.text for element in elements]
#     return items_list
