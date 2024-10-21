class HomePageData:
    """
    Class to hold test data for the Home Page login functionality,
    including valid/invalid users and expected error messages for different failure scenarios.
    """

    test_home_page_login = [
        {
            'user_name_hint': 'Username',  # Placeholder text for the username field
            'pw_hint': 'Password',  # Placeholder text for the password field

            # Set of valid users for testing successful login
            'users': [
                'standard_user',  # A user with standard access privileges
                'problem_user',  # A user experiencing problems
                'performance_glitch_user',  # A user that encounters performance issues
                'error_user',  # A user that causes errors
                'visual_user'  # A user with visual accessibility needs
            ],

            # Tuple of invalid usernames for testing unsuccessful login attempts
            'invalid_users': (
                'Darth_Vaders_Nephew',  # Fictional username
                'standard_users ',  # Trailing space, should be invalid
                ' standard_user',  # Leading space, should be invalid
                'standard_user '  # Trailing space, should be invalid
            ),

            'locked_user': 'locked_out_user',  # Username that should be locked out from logging in

            'password': 'secret_sauce',  # Valid password used for logging in

            # Tuple of invalid passwords for testing unsuccessful login attempts
            'invalid_passwords': (
                'bs password',  # Completely invalid password
                '*secret_sauce',  # Special character added, making it invalid
                ' secret_sauce',  # Leading space, should be invalid
                'secret_sauce '  # Trailing space, should be invalid
            ),

            # Expected error messages for various invalid login scenarios
            'expected_error_messages': {
                'empty_username': "Epic sadface: Username is required",
                'empty_password': "Epic sadface: Password is required",
                'invalid_credentials': "Epic sadface: Username and password do not match any user in this service",
                'locked_user': "Epic sadface: Sorry, this user has been locked out."
            }
        }
    ]

    test_login_latency = [
        {

            # Set of valid users for testing successful login
            'users': [
                'standard_user',  # A user with standard access privileges
                'problem_user',  # A user experiencing problems
                'performance_glitch_user',  # A user that encounters performance issues
                'error_user',  # A user that causes errors
                'visual_user'  # A user with visual accessibility needs
            ],

            'password': 'secret_sauce',  # Valid password used for logging in

            }

    ]


    # @staticmethod
    # def get_data(self, request):
    #     return request.param

    # @staticmethod
    # def get_data_excel(test_case):
    #
    #     #path_to_excell = r'C:\Users\hkfir\PycharmProjects\pythonKfirFramework\TestData\ExcelDataToPytest.xlsx'
    #     path_to_excell = '/app/TestData/ExcelDataToPytest.xlsx'  # TODO remove app/ when running locally
    #     book = openpyxl.load_workbook(path_to_excell)
    #     sheet = book.active
    #
    #     test_list = []
    #
    #     for rw in range(1, sheet.max_row + 1):
    #         test_data = {}
    #         if sheet.cell(row=rw, column=1).value == test_case:
    #             for cl in range(2, sheet.max_column + 1):
    #                 test_data[sheet.cell(row=1, column=cl).value] = sheet.cell(row=rw, column=cl).value
    #             test_list.append(test_data)
    #     return test_list
