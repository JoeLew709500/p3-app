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
    To select which search you would like to do on a request
    """
    menu=True

    while menu:
        print('1. Search by request ID\n2. Search by received date\n3. Search by completed date\n4. Search by type')
        selection = input('Please enter the number of what you would like to search by \n')
        if selection == '1':
            find_request_by_id()
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

def find_request_by_id():
    """
    Get request details from id number
    """

    id = input('What is the request id you would like to view? \n')
    # Finds the id and stores what cell that id is in
    cell = requests.find(id,in_column=1)

    row = cell.row

    get_request_details(id,row)

def get_request_details(id,row):

    date_received = requests.cell(row,4).value
    date_completed = requests.cell(row,5).value
    text = requests.cell(row,6).value
    type = requests.cell(row,7).value
    time_to_complete = requests.cell(row,8).value

    print(f'Request ID: {id}\nDate Received: {date_received}\nDate Completed: {date_completed}\nRequest Details: {text}\nType: {type}\nTime to complete: {time_to_complete} days')

find_request_menu()