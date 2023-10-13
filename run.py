import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('applicationDB')

requests = SHEET.worksheet('requests')
actions = SHEET.worksheet('actions')
contact = SHEET.worksheet('contact')
location = SHEET.worksheet('location')

def find_request_menu():
    """
    To search and display request information
    """
    menu=True

    while menu:
        print('1. Search by request ID\n2. Search by received date\n3. Search by completed date\n4. Search by type')
        selection = input('Please enter the number of what you would like to search by ')
        if selection == '1':
            print('Selected 1')
            menu = False
        elif selection == '2':
            print('Selected 2')
            menu = False
        elif selection == '3':
            print('Selected 3')
            menu = False
        elif selection == '4':
            print('Selected 4')
            menu = False
        else:
            print(f'Invalid selection: You selected {selection} please try again')


