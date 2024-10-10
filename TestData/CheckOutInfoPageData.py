class CheckOutInfoPageData:
    test_submit_page = [

        {
            # Expected error messages for various submit actions
            'expected_error_messages': {
                'empty_name': "Error: First Name is required",
                'empty_last_name': "Error: Last Name is required",
                'empty_postal': "Error: Postal Code is required",
            }
        }
    ]
