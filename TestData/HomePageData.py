import openpyxl

class HomePageData:

    test_home_page_date_submit = [
        {'first_name': 'Kfir',
         'password': 'password1',
         'email': 'kelogs@fast.com',
         'gender': 'Male',
         'employment_stat': 'Student'},
        {'first_name': 'Ifat',
         'password': 'passw0rd2',
         'email': 'none@gmail.com',
         'gender': 'Female',
         'employment_stat': 'Employed'}]

    @staticmethod
    def get_data_excel(test_case):

       #path_to_excell = r'C:\Users\hkfir\PycharmProjects\pythonKfirFramework\TestData\ExcelDataToPytest.xlsx'
        path_to_excell = 'TestData/ExcelDataToPytest.xlsx'
        book = openpyxl.load_workbook(path_to_excell)
        sheet = book.active

        test_list = []

        for rw in range(1, sheet.max_row + 1):
            test_data = {}
            if sheet.cell(row=rw, column=1).value == test_case:
                for cl in range(2, sheet.max_column + 1):
                    test_data[sheet.cell(row=1, column=cl).value] = sheet.cell(row=rw, column=cl).value
                test_list.append(test_data)
        return test_list
