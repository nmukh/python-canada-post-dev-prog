"""
api_details_blank.py

Copy this file to api_details.py and fill in the user details necessary to run
the tests.

"""

from canada_post import Auth, DEV

# Enter your developer program information here
AUTH = Auth(
    customer_number = "",   # (required for all tests)
    username = "",          # (required for all tests) Username portion of the
                            # API key you wish to use
    password = "",          # (required for all tests) Password portion of the
                            # API key you wish to use
    contract_number = "",   # required for contract shipping (maybe)
    dev = DEV)
